from twisted.web import http
from twisted.web.http import HTTPChannel
from twisted.internet import reactor
import threading

class BotHandler(http.Request, object):
    def __init__(self, api, *args, **kwargs):
        self.api = api
        super(BotHandler, self).__init__(*args, **kwargs)

    def render(self, content, headers):
        for (header_name, header_value) in headers:
            self.setHeader(header_name, header_value)
        self.write(content)
        self.finish()

    def simple_render(self, content, content_type="text/plain"):
        self.render(content, [("Content-Type", content_type)])

    def not_found(self, message=None):
        self.setResponseCode(404, message)
        return self.simple_render("no no...")

    def process(self):
        command_args_list = [x for x in self.path.split("/") if x]
        command = ""
        args = []
        if command_args_list:
            command = command_args_list[0]
            args = command_args_list[1:]

        try:
            if not command:
                f = open("main.html")
                content = f.read()
                return self.simple_render(content, content_type="text/html")
            if command.startswith("wave"):
                amount = int(args[0]) if len(args) > 0 else 1
                for x in range(amount):
                    if command == "wave_short":
                        self.api.trigger("wave", min=0.3, max=0.7)
                    else:
                        self.api.trigger("wave")
                return self.simple_render(" ".join(["Wave and smile."]*amount))
            elif command == "set":
                self.api.trigger("set", position=float(args[0]))
                return self.simple_render("ok")
        except Exception, e:
            return self.simple_render(e.message)

        return self.not_found()


class BotHandlerFactory(object):
    def __init__(self, api):
        self.api = api

    def __call__(self, *args, **kwargs):
        return BotHandler(self.api, *args, **kwargs)


class StreamFactory(http.HTTPFactory):
    protocol = HTTPChannel


class Api:
    """ An api for attentionbot, uses a twisted server inside a thread to keep track of webby things. """

    def __init__(self):
        # This I believe is what you find when you look up "ugly" in the dictionary
        # But I really don't want to try and understand this FactoryFactoryFactory stuff properly
        HTTPChannel.requestFactory = BotHandlerFactory(api=self)

        self.events = []

    def demonize(self, port=8080):
        reactor.listenTCP(port, StreamFactory())
        t = threading.Thread(target=reactor.run)
        t.daemon = True
        t.start()

    def run(self, port=8080):
        reactor.listenTCP(port, StreamFactory())
        reactor.run()

    def trigger(self, event, **kwargs):
        for x in range(len(self.events)):
            if self.events[x][0] == event:
                self.events[x] = (event, kwargs)
                return
        self.events.append((event, kwargs))
                                              