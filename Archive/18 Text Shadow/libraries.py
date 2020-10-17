import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def add_subtitle(
    bg,
    text,
    xy,
    font="C:\Users\Andrew Ke\Downloads\Oswald\static\Oswald-SemiBold.ttf",
    font_size=53,
    font_color=(255, 255, 255),
    stroke=2,
    stroke_color=(0, 0, 0),
    shadow=(4, 4),
    shadow_color=(0, 0, 0),
):
    """draw subtitle on image by pillow
    Args:
        bg(PIL image): image to add subtitle
        text(str): subtitle
        xy(tuple): absolute top left location of subtitle
        ...: extra style of subtitle
    Returns:
        bg(PIL image): image with subtitle
    """

    color_coverted = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    bg = Image.fromarray(color_coverted)

    stroke_width = stroke
    xy = list(xy)
    W, H = bg.width, bg.height
    font = ImageFont.truetype(str(font), font_size)
    w, h = font.getsize(text, stroke_width=stroke_width)
    if xy[0] == "center":
        xy[0] = (W - w) // 2
    if xy[1] == "center":
        xy[1] = (H - h) // 2
    draw = ImageDraw.Draw(bg)
    if shadow:
        draw.text(
            (xy[0] + shadow[0], xy[1] + shadow[1]), text, font=font, fill=shadow_color
        )
    draw.text(
        (xy[0], xy[1]),
        text,
        font=font,
        fill=font_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color,
    )

    # use numpy to convert the pil_image into a numpy array
    numpy_image=np.array(bg)  

    # convert to a openCV2 image, notice the COLOR_RGB2BGR which means that 
    # the color is converted from RGB to BGR format
    bg=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR) 


    return bg

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    # return cv2.resize(image, dim, interpolation=cv2.INTER_NEAREST)
    return cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)    



from threading import Thread
import sys
# import cv2
import time

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue


#multithread video decode and downscale to 720p
class FileVideoStream: 
    # def __init__(self, path, transform=None, queue_size=128):
    def __init__(self, path, transform=None, queue_size=196):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        # self.stream = cv2.VideoCapture(path, cv2.CAP_MSMF)

        self.stopped = False
        self.transform = transform

        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queue_size)
        # intialize thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True

    def start(self):
        # start a thread to read frames from the file video stream
        self.thread.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                break

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stopped = True
                    
                # if there are transforms to be done, might as well
                # do them on producer thread before handing back to
                # consumer thread. ie. Usually the producer is so far
                # ahead of consumer that we have time to spare.
                #
                # Python is not parallel but the transform operations
                # are usually OpenCV native so release the GIL.
                #
                # Really just trying to avoid spinning up additional
                # native threads and overheads of additional
                # producer/consumer queues since this one was generally
                # idle grabbing frames.
                if self.transform:
                    frame = self.transform(frame)

                frame = ResizeWithAspectRatio(frame, width=1280) #slow function, about 2.5ms
                # add the frame to the queue
                self.Q.put(frame)
            else:
                time.sleep(0.1)  # Rest for 10ms, we have a full queue

        self.stream.release()

    def read(self):
        # return next frame in the queue
        return self.Q.get()

    # Insufficient to have consumer use while(more()) which does
    # not take into account if the producer has reached end of
    # file stream.
    def running(self):
        return self.more() or not self.stopped

    def more(self):
        # return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
        tries = 0
        while self.Q.qsize() == 0 and not self.stopped and tries < 5:
            time.sleep(0.1)
            tries += 1

        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        # wait until stream resources are released (producer thread might be still grabbing frame)
        self.thread.join()    