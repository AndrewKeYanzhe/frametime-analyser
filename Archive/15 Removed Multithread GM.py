# -*- coding: utf-8 -*-
import time
import numpy as np
import cv2
from skimage.measure import compare_ssim
import matplotlib.pyplot as plt

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

#my red dead gameplay
# cap = cv2.VideoCapture("F:/ReLive/2020.09.18-22.33.mp4", cv2.CAP_MSMF)
# cap = cv2.VideoCapture("F:/ReLive/2020.09.18-22.33.mp4")
cap = cv2.VideoCapture("F:/ReLive/rdr2 h264.m4v")
#my ACO gameplay
# cap = cv2.VideoCapture("F:/ReLive/2020.09.24-21.36.mp4")
# cap = cv2.VideoCapture("E:/Downloads/The Last of Us 2 - What 60fps Gameplay Looks Like.mp4")
# cap = cv2.VideoCapture("E:/Downloads/COSTA RICA IN 4K 60fps HDR (ULTRA HD).mp4")
# cap = cv2.VideoCapture("E:\Downloads\Demon's Souls -  Official 4K 60Fps Gameplay Trailer-1.m4v")

pause_frame = False
pause_frame = True


TIMEOUT = 1/60
old_timestamp = time.time()

count = 0
frametime = 0
frametime_display = "None"
# total_dropped = 0

graph_width = 60
frametime_graph = [0]*graph_width
before_showing = None

while(cap.isOpened()):
    # s1 = cv2.getTickCount()

    ret, frame = cap.read()
    
   

    if count == 0:
        prev_frame = frame
        height = len(frame)
        width = len(frame[0])
        before_showing = cv2.getTickCount()


    scale = 0.1
    # SCREENCAP  downscale only
    cropped_frame = cv2.resize(frame, (0,0), fx=scale, fy=scale)
    cropped_prev_frame = cv2.resize(prev_frame, (0,0), fx=scale, fy=scale) 

    # cropped_frame = frame
    # cropped_prev_frame = prev_frame


    cropped_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
    cropped_prev_frame = cv2.cvtColor(cropped_prev_frame, cv2.COLOR_BGR2GRAY)

    

    frame_diff = cv2.absdiff(cropped_frame, cropped_prev_frame)
    average = frame_diff.mean(axis=0).mean(axis=0)

    # print average

    #FOR SCREENCAP
    threshold = 0.8
    if average < threshold:
        result = "Dropped"
    else:
        # result = "Unique"
        result = ""
        frametime_display = frametime
        frametime_graph.pop(0)
        frametime_graph.append(frametime)
        # print frametime_graph

        frametime = 0


    texted_image =cv2.putText(frame, text='{:4.2f}'.format(average)+" "+str(frametime_display)+" "+result, org=(200,200),fontFace=3, fontScale=3, color=(0,0,255), thickness=5)



    resize = ResizeWithAspectRatio(texted_image, width=1280) #slow function, about 2.5ms

    pt_width = 2
    pt_spacing = 2
    pt_gap = pt_spacing - pt_width
    ft_color = (93, 232, 130)
    plt_origin_x = 60
    plt_origin_y = 480
    for key, value in enumerate(frametime_graph):
        if value == 0:
            continue
        prev_ft = frametime_graph[key-1]
        cv2.line(resize,(plt_origin_x + key*pt_spacing, plt_origin_y-value*10),(plt_origin_x + key*pt_spacing + pt_width, plt_origin_y-value*10),ft_color,1)
        if key !=0:
            cv2.line(resize,(plt_origin_x + key*pt_spacing - pt_gap, plt_origin_y- prev_ft*10),(plt_origin_x + key*pt_spacing, plt_origin_y-value*10),ft_color,1)

    cv2.rectangle(resize,(plt_origin_x,plt_origin_y-60),(plt_origin_x+graph_width*pt_spacing,plt_origin_y),(255,255,255),1)
    cv2.putText(resize, text="16.7", org=(plt_origin_x+graph_width*pt_spacing+10,plt_origin_y-5),fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255,255,255), thickness=1)

    
   	

    #Calculate total time elapse since Vsync, performance analysis
    # calc_time = (cv2.getTickCount() - before_showing)/ cv2.getTickFrequency()*1000
    # if calc_time>1000/60:
    #     print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # print calc_time
    # print "----"
      
    # print (s2 - before_showing)/ cv2.getTickFrequency()*1000 #perfromance

    #vsync
    while ((cv2.getTickCount() - before_showing)/cv2.getTickFrequency()*10**6< 10**6/60.01):

        continue
    # print (cv2.getTickCount() - before_showing)/cv2.getTickFrequency()*1000 #check if equal 16.666, disable to ensure vsync works
    before_showing = cv2.getTickCount()
    cv2.imshow('frame',resize)
    
    





    prev_ret, prev_frame = ret, frame
    count = count + 1
    frametime = frametime + 1

    s2 = cv2.getTickCount()

    # print "---"  

    if pause_frame:
	    if cv2.waitKey(0) & 0xFF == ord('q'):
        	break
    else:    
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
        

cap.release()
cv2.destroyAllWindows()