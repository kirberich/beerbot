import time
import cv2, cv
import numpy

DEBUG = True

class Recorder(object):
    def __init__(self, limit_fps=None):
        self.last_video_frame = None
        self.current_jpg_frame = None

        self.keep_running = True
        self.frame_rate = 0
        self.last_frame = time.time()
        self.limit_fps = limit_fps

    def update_frame_rate(self):
        # FIXME: save some kind of average for the fps
        self.frame_diff = time.time() - self.last_frame

        if self.limit_fps:
            minimum_frame_diff = 1.0/self.limit_fps
            if self.frame_diff < minimum_frame_diff:
                time.sleep(minimum_frame_diff - self.frame_diff)
            self.frame_diff = time.time() - self.last_frame

        self.frame_rate = 1.0/self.frame_diff
        self.last_frame = time.time()

        if DEBUG:
            print "FPS: %s" % round(self.frame_rate)

    def buffer_frame(self, frame):
        (retval, jpg_frame) = cv2.imencode(".jpg", frame, (cv.CV_IMWRITE_JPEG_QUALITY, 50))
        jpg_frame = jpg_frame.tostring()
        self.current_jpg_frame = jpg_frame

    def loop(self):
        while self.keep_running:
            self.update_frame_rate()
            self.handle_frame()

    def capture_frame(self, as_array=True):
        raise NotImplementedError()

    def handle_frame(self, *args, **kwargs):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()


class CVCaptureRecorder(Recorder):
    def __init__(self, limit_fps=None):
        super(CVCaptureRecorder, self).__init__(limit_fps)
        self.capture = cv.CaptureFromCAM(0)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

        if self.capture: # try to get the first frame
            frame = cv.QueryFrame(self.capture)
        else:
            raise Exception("Could not open video device")

    def capture_frame(self, as_array=True):
        frame = cv.QueryFrame(self.capture)
        if not as_array:
            return frame
        frame_array = numpy.asarray(frame[:,:])
        return frame_array

    def handle_frame(self):
        frame = self.capture_frame(as_array=False)
        frame_array = numpy.asarray(frame[:,:])

        self.buffer_frame(frame_array)
