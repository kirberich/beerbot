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
            elif command == "set":
                print "direction"
                self.api.trigger("set", position=float(args[0]))
                return self.simple_render("ok")
            elif command == "set_speed":
                print "speed"
                self.api.trigger("set_speed", position=float(args[0]))
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
        self.lock = threading.Lock()

    def demonize(self, port=8080):
        reactor.listenTCP(port, StreamFactory())
        t = threading.Thread(target=reactor.run)
        t.daemon = True
        t.start()

    def run(self, port=8080):
        reactor.listenTCP(port, StreamFactory())
        reactor.run()

    def trigger(self, event, **kwargs):
        with self.lock:
            for x in range(len(self.events)):
                if self.events[x][0] == event:
                    self.events[x] = (event, kwargs)
                    return
            self.events.append((event, kwargs))

