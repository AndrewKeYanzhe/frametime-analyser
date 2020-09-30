# -*- coding: utf-8 -*-
import time
import numpy as np
import cv2
from skimage.measure import compare_ssim

def is_similar(image1, image2):
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

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

# cap = cv2.VideoCapture("E:/Downloads/The Last of Us Part II – E3 2018 Gameplay Reveal Trailer  4k PS4.mkv")

def crop_and_join(frame):
    fr_h = len(frame)
    fr_w = len(frame[0])

    #a1a2a3
    #b1b2b3
    #c1c2c3

    #crop height
    c_h = int(fr_h*0.1)
    c_w = int(fr_w*0.1)

    mid_w = int(fr_w*0.45)
    right_w = int(fr_w*0.9)

    mid_h = int(fr_h*0.45)
    bottom_h = int(fr_h*0.9)



    a1=frame[0:c_h, 0:                  c_w]
    a2=frame[0:c_h, mid_w:mid_w+        c_w]
    a3=frame[0:c_h, right_w:right_w+    c_w]
    b1=frame[mid_h : mid_h + c_h, 0:                  c_w]
    b2=frame[mid_h : mid_h + c_h, mid_w:mid_w+        c_w]
    b3=frame[mid_h : mid_h + c_h, right_w:right_w+    c_w]    
    c1=frame[bottom_h : bottom_h + c_h, 0:                  c_w]
    c2=frame[bottom_h : bottom_h + c_h, mid_w:mid_w+        c_w]
    c3=frame[bottom_h : bottom_h + c_h, right_w:right_w+    c_w]

    a = np.concatenate((a1, a2, a3), axis=1)
    b = np.concatenate((b1, b2, b3), axis=1)
    c = np.concatenate((c1, c2, c3), axis=1)
    result = np.concatenate((a, b,c), axis=0)

    return result

count = 0
frametime = 0
frametime_display = "None"
# total_dropped = 0

while(cap.isOpened()):
    ret, frame = cap.read()

    if count == 0:
        prev_frame = frame
        height = len(frame)
        width = len(frame[0])

    # # SCREENCAP crop, join and downscale
    # cropped_frame = crop_and_join(frame)      
    # cropped_prev_frame = crop_and_join(prev_frame)
    # #downscale
    # cropped_frame = cv2.resize(cropped_frame, (0,0), fx=0.5, fy=0.5)
    # cropped_prev_frame = cv2.resize(cropped_prev_frame, (0,0), fx=0.5, fy=0.5) 

    # SCREENCAP  downscale only
    # cropped_frame = crop_and_join(frame)      
    # cropped_prev_frame = crop_and_join(prev_frame)
    #downscale
    cropped_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.1)
    cropped_prev_frame = cv2.resize(prev_frame, (0,0), fx=0.5, fy=0.1) 

    # #FOR iPHONE 4k60 far
    # cropped_frame = frame[800:1200, 1600:2400]
    # cropped_prev_frame = prev_frame[800:1200, 1600:2400]
    # # downscale
    # cropped_frame = cv2.resize(cropped_frame, (0,0), fx=0.5, fy=0.5)
    # cropped_prev_frame = cv2.resize(cropped_prev_frame, (0,0), fx=0.5, fy=0.5) 


    grey_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
    grey_prev_frame = cv2.cvtColor(cropped_prev_frame, cv2.COLOR_BGR2GRAY)

    # grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # grey_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # print grey_frame

    (score, diff) = compare_ssim(grey_frame, grey_prev_frame, full=True)
    # diff = (diff * 255).astype("uint8")
    # print("SSIM: {}".format(score))
    # similarity = is_similar(frame, prev_frame)



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
    # cv2.imshow('frame',cropped_frame)
    cv2.imshow('frame',resize)


    prev_ret, prev_frame = ret, frame
    count = count + 1
    frametime = frametime + 1
    

    # cv2.waitKey(0)



    # time.sleep(0.2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()