# -*- coding: utf-8 -*-
import time
import numpy as np
import cv2
from skimage.measure import compare_ssim


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
    return cv2.resize(image, dim, interpolation=inter)

#my red dead gameplay
cap = cv2.VideoCapture("F:/ReLive/2020.09.18-22.33.mp4")

#my ACO gameplay
# cap = cv2.VideoCapture("F:/ReLive/2020.09.24-21.36.mp4")

# cap = cv2.VideoCapture("E:/Downloads/The Last of Us Part II – E3 2018 Gameplay Reveal Trailer  4k PS4.mkv")

TIMEOUT = 0.0333333333333333333333333333
old_timestamp = time.time()

count = 0
frametime = 0
frametime_display = "None"
# total_dropped = 0

while(cap.isOpened()):
    e1 = cv2.getTickCount()

    ret, frame = cap.read()

    if count == 0:
        prev_frame = frame
        height = len(frame)
        width = len(frame[0])


    scale = 0.2
    # SCREENCAP  downscale only
    cropped_frame = cv2.resize(frame, (0,0), fx=scale, fy=scale)
    cropped_prev_frame = cv2.resize(prev_frame, (0,0), fx=scale, fy=scale) 

    # #FOR iPHONE 4k60 far
    # cropped_frame = frame[800:1200, 1600:2400]
    # cropped_prev_frame = prev_frame[800:1200, 1600:2400]
    # # downscale
    # cropped_frame = cv2.resize(cropped_frame, (0,0), fx=0.5, fy=0.5)
    # cropped_prev_frame = cv2.resize(cropped_prev_frame, (0,0), fx=0.5, fy=0.5) 


    cropped_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
    cropped_prev_frame = cv2.cvtColor(cropped_prev_frame, cv2.COLOR_BGR2GRAY)

    
    (score, diff) = compare_ssim(cropped_frame, cropped_prev_frame, full=True)
    # diff = (diff * 255).astype("uint8")
    # print("SSIM: {}".format(score))




    #FOR SCREENCAP
    threshold = 0.99
    if score > threshold:
        result = "Dropped"
    else:
        # result = "Unique"
        result = ""
        frametime_display = frametime
        frametime = 0

    # #FOR iphone recorded 4k60 close to screen
    # threshold = 0.9
    # if score > threshold:
    #     result = "Dropped"
    # else:
    #     # result = "Unique"
    #     result = ""
    #     frametime_display = frametime
    #     frametime = 0



    texted_image =cv2.putText(frame, text='{:4.2f}'.format(score)+" "+str(frametime_display)+" "+result, org=(200,200),fontFace=3, fontScale=3, color=(0,0,255), thickness=5)

    resize = ResizeWithAspectRatio(texted_image, width=1280)

    
    

    # too_slow = "too slow"
    e2 = cv2.getTickCount()
    print (e2 - e1)/ cv2.getTickFrequency()
    while(True):
        if (time.time() - old_timestamp) > TIMEOUT:
            # print count
            # print too_slow

            # cv2.imshow('frame',cropped_frame)
            cv2.imshow('frame',resize)

            old_timestamp = time.time()


            prev_ret, prev_frame = ret, frame
            count = count + 1
            frametime = frametime + 1
            

            # cv2.waitKey(0)
            break


        # too_slow = "ok"

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

cap.release()
cv2.destroyAllWindows()