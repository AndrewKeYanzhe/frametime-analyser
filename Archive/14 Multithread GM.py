# '.\14 Multithread GM.py' --video "F:/ReLive/2020.09.18-22.33.mp4"



# -*- coding: utf-8 -*-
import time
import numpy as np
import cv2
from skimage.measure import compare_ssim
import matplotlib.pyplot as plt

from libraries import *



# def Read 
#my red dead gameplay
# file_path = "F:/ReLive/2020.09.18-22.33.mp4"
#my ACO gameplay
# file_path = "F:/ReLive/2020.09.24-21.36.mp4"
file_path = "E:/Downloads/The Last of Us 2 - What 60fps Gameplay Looks Like.mp4"
file_path = "F:/ReLive/rdr2 h264.m4v"

# file_path = "E:/Downloads/COSTA RICA IN 4K 60fps HDR (ULTRA HD).mp4"





count = 0
frametime = 0
frametime_display = "None"
# total_dropped = 0

graph_width = 60
frametime_graph = [0]*graph_width
before_showing = None




# import the necessary packages
# from imutils.video import FileVideoStream
# from imutils.video import FPS
# import numpy as np
import argparse
# import imutils
import time
# import cv2




# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", required=True,
#     help="path to input video file")
# args = vars(ap.parse_args())
# # start the file video stream thread and allow the buffer to
# # start to fill
# print("[INFO] starting video file thread...")
# print args




# fvs = FileVideoStream(args["video"]).start()
fvs = FileVideoStream(file_path).start()
time.sleep(3)
# start the FPS timer
# fps = FPS().start()


before_showing = cv2.getTickCount()
# while(cap.isOpened()):
while fvs.more():   

    frame = fvs.read()
    





    #print the size of the queue on the frame
    print "Queue Size: {}".format(fvs.Q.qsize())
   

    if count == 0:
        prev_frame = frame
        height = len(frame)
        width = len(frame[0])
        
    


    #DOWN SCALING
    # scale = 0.1
    scale = 0.02    
    cropped_frame = cv2.resize(frame, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    cropped_prev_frame = cv2.resize(prev_frame, (0,0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

    #NO DOWN SCALING
    # cropped_frame = frame
    # cropped_prev_frame = prev_frame




    


    # #FOR iPHONE 4k60 far
    # cropped_frame = frame[800:1200, 1600:2400]
    # cropped_prev_frame = prev_frame[800:1200, 1600:2400]
    # # downscale
    # cropped_frame = cv2.resize(cropped_frame, (0,0), fx=0.5, fy=0.5)
    # cropped_prev_frame = cv2.resize(cropped_prev_frame, (0,0), fx=0.5, fy=0.5)



    cropped_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
    cropped_prev_frame = cv2.cvtColor(cropped_prev_frame, cv2.COLOR_BGR2GRAY)

    

    frame_diff = cv2.absdiff(cropped_frame, cropped_prev_frame)
    average = frame_diff.mean(axis=0).mean(axis=0)
    



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

    

    text_to_draw = '{:4.2f}'.format(average)+" "+str(frametime_display)+" "+str(fvs.Q.qsize())+ " "+result
    texted_image =cv2.putText(frame, text=text_to_draw, org=(200,200),fontFace=3, fontScale=3, color=(0,0,255), thickness=5)
    texted_image = frame


    print (cv2.getTickCount() - before_showing)/ cv2.getTickFrequency()*1000 #PASTE to test perf    

    # resize = ResizeWithAspectRatio(texted_image, width=1280) #slow function, about 2.5ms
    resize = texted_image

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


    # s2 = cv2.getTickCount()
    #analyse section for performance
    # print (s2 - before_showing)/ cv2.getTickFrequency()*1000

    #Calculate total time elapse since Vsync, performance analysis
    calc_time = (cv2.getTickCount() - before_showing)/ cv2.getTickFrequency()*1000
    if calc_time>1000/60:
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # print calc_time
      
    prev_frame = frame
    count = count + 1
    frametime = frametime + 1
    
    #vsync
    while ((cv2.getTickCount() - before_showing)/cv2.getTickFrequency()*10**6< 10**6/60.01):
        continue
        
    # print (cv2.getTickCount() - before_showing)/cv2.getTickFrequency()*1000 #check if equal 16.666, disable to ensure vsync works
    before_showing = cv2.getTickCount()
    cv2.imshow('frame',resize)
    
    






    # cv2.waitKey(1)


    

    # print "---"  
    # if cv2.waitKey(0) & 0xFF == ord('q'):
    if cv2.waitKey(1) & 0xFF == ord('q'):

        break
    

cap.release()
cv2.destroyAllWindows()