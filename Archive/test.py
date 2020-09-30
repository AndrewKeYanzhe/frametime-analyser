# -*- coding: utf-8 -*-
import time
import numpy as np
import cv2
from skimage.measure import compare_ssim
import matplotlib.pyplot as plt
from threading import Thread



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
    return cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True


def threadVideoGet(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Main thread shows video frames.
    """

    video_getter = VideoGet(source).start()
    # cps = CountsPerSec().start()

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

        frame = video_getter.frame
        # frame = putIterationsPerSec(frame, cps.countsPerSec())
        # cv2.imshow("Video", frame)
        # cps.increment()
        return frame





#my red dead gameplay
cap = cv2.VideoCapture("F:/ReLive/2020.09.18-22.33.mp4")
#my ACO gameplay
# cap = cv2.VideoCapture("F:/ReLive/2020.09.24-21.36.mp4")
# cap = cv2.VideoCapture("E:/Pictures/2018-12-11 USA (Phone)/iPhone X/IMG_0100.MOV")
cap = cv2.VideoCapture("E:/Downloads/COSTA RICA IN 4K 60fps HDR (ULTRA HD).mp4")
# TIMEOUT = 0.0166666666666666666666666666666666666666666
TIMEOUT = 0
old_timestamp = time.time()

count = 0
frametime = 0
frametime_display = "None"


graph_width = 60
frametime_graph = [0]*graph_width


while(cap.isOpened()):
    e1 = cv2.getTickCount()

    ret, frame = cap.read()
    
    cv2.imshow('frame',frame)



    e2 = cv2.getTickCount()
    print (e2 - e1)/ cv2.getTickFrequency()*1000    
    print "---"

    



    if cv2.waitKey(7) & 0xFF == ord('q'):
        break
        

cap.release()
cv2.destroyAllWindows()