# -*- coding: utf-8 -*-
import time
import numpy as np
import cv2
from skimage.measure import compare_ssim
import matplotlib.pyplot as plt

pause_frame = False 
# pause_frame = True #wait for keypress before playing next frame

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

#RDR2 capture
# cap = cv2.VideoCapture("F:/ReLive/2020.09.18-22.33.mp4", cv2.CAP_MSMF)	#worse decoder
# cap = cv2.VideoCapture("F:/ReLive/2020.09.18-22.33.mp4")
# cap = cv2.VideoCapture("E:\Downloads\Xiaomi Yi 4K 2 1080p 60fps ultra wide stabilization on sample.mp4")
# cap = cv2.VideoCapture("F:/ReLive/rdr2 h264.m4v") #transcoded HEVC to h264

#ACO capture
cap = cv2.VideoCapture("F:/ReLive/2020.09.24-21.36.mp4")

# cap = cv2.VideoCapture("E:/Downloads/The Last of Us 2 - What 60fps Gameplay Looks Like.mp4")
# cap = cv2.VideoCapture("E:/Downloads/COSTA RICA IN 4K 60fps HDR (ULTRA HD).mp4")
# cap = cv2.VideoCapture("E:\Downloads\GTA 5 ►RTX 3090 8k 60fps MAX SETTINGS With Ray Tracing Ultra Graphics Mod! GTA 6 Level PC Graphics!.mp4")

count = 0
frametime = 0
frametime_text = "None"

graph_width = 60 #width of grametime graph

frametime_graph = [0]*graph_width #list of previous frametimes
before_showing = None #timestamp to be taken before cv2.imshow
moving_avg = 0	#exponentially decaying moving avg for previous frametimes
fps_list = [0]*60
fps = 0
fps_graph_samples = 580
fps_graph = [0]*fps_graph_samples


while(cap.isOpened()):
    ret, frame = cap.read() 

    if count == 0:
        prev_frame = frame
        height = len(frame)
        width = len(frame[0])
        before_showing = cv2.getTickCount()

    #downscale before calculating difference
    scale = 0.1
    cropped_frame = cv2.resize(frame, (0,0), fx=scale, fy=scale)
    cropped_prev_frame = cv2.resize(prev_frame, (0,0), fx=scale, fy=scale) 
    #convert to grayscale
    cropped_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
    cropped_prev_frame = cv2.cvtColor(cropped_prev_frame, cv2.COLOR_BGR2GRAY)

    #calculate frame difference
    frame_diff = cv2.absdiff(cropped_frame, cropped_prev_frame)
    average = frame_diff.mean(axis=0).mean(axis=0)
    if count == 1:
    	moving_avg = average
    	
    # print average

    threshold = 0.25*moving_avg #threshold below which a frame is considered "identical" or dropped

    if average < threshold:
    	fps_list.pop(0)
    	fps_list.append(0)
    	fps = sum(fps_list)

    	fps_graph.pop(0)
    	fps_graph.append(fps)
    else:
        result = ""
        frametime_text = frametime
        frametime_graph.pop(0)
        frametime_graph.append(frametime)
        
        fps_list.pop(0)
    	fps_list.append(1)
    	fps = sum(fps_list)

    	fps_graph.pop(0)
    	fps_graph.append(fps)
        # print frametime_graph
        frametime = 0	#frametime will be incremented at end of loop
    # print fps
    # print fps_list
    if(count)<60:
    	fps = ""
    # print (average, moving_avg, result)
    moving_avg = (moving_avg + average/3)*3/4



    # text_to_write = '{:4.2f}'.format(average)+" "+str(frametime_text)+" "+result
    # texted_image =cv2.putText(frame, text=text_to_write, org=(200,200),fontFace=3, fontScale=3, color=(0,0,255), thickness=5)
    
 

    text_to_write = str(fps)
    texted_image =cv2.putText(frame, text=text_to_write, org=(1750,150),fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(255,255,255), thickness=5)

    resize = ResizeWithAspectRatio(texted_image, width=1280) #slow function, about 2.5ms

    #drawing frametime graph
    pt_width = 2
    pt_spacing = 2
    pt_gap = pt_spacing - pt_width
    ft_color = (93, 232, 130)
    plt_origin_x = 60
    plt_origin_y = 480
    y_scale = 20

    # print frametime_graph
    for key, value in enumerate(frametime_graph):

        prev_ft = frametime_graph[key-1]
        if key ==0:
        	continue
        if prev_ft == 0:
            continue        
        cv2.line(resize,(plt_origin_x + key*pt_spacing, plt_origin_y-value*y_scale),(plt_origin_x + key*pt_spacing + pt_width, plt_origin_y-value*y_scale),ft_color,1)
        if key !=0:
            cv2.line(resize,(plt_origin_x + key*pt_spacing - pt_gap, plt_origin_y- prev_ft*y_scale),(plt_origin_x + key*pt_spacing, plt_origin_y-value*y_scale),ft_color,1)
    cv2.rectangle(resize,(plt_origin_x,plt_origin_y-60),(plt_origin_x+graph_width*pt_spacing,plt_origin_y-10),(255,255,255),1)
    cv2.putText(resize, text="16.7", org=(plt_origin_x+graph_width*pt_spacing+10,plt_origin_y-15),fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255,255,255), thickness=1)
    cv2.putText(resize, text="33.3", org=(plt_origin_x+graph_width*pt_spacing+10,plt_origin_y- 15 - y_scale),fontFace=cv2.	FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255,255,255), thickness=1)
    cv2.putText(resize, text="FRAME-TIME (MS)", org=(plt_origin_x,plt_origin_y -70),fontFace=cv2.	FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255,255,255), thickness=1)

    plt_origin_x = 60
    plt_origin_y = 500
    pt_width = 0
    pt_spacing = 2
    pt_gap = pt_spacing - pt_width
    y_scale = 4

    graph_speed = 2

    for key, value in enumerate(fps_graph):
        if count<fps_graph_samples-key+60:
            continue
        if key == 0:
        	continue
        prev_ft = fps_graph[key-1]
        start_point = plt_origin_x + key*graph_speed		, plt_origin_y-(prev_ft-60)*y_scale
        end_point 	= plt_origin_x + (key+1)*graph_speed	, plt_origin_y-(value-60)*y_scale
        cv2.line(resize,(start_point),(end_point),ft_color,2)
    cv2.rectangle(resize,(plt_origin_x,plt_origin_y),(plt_origin_x+fps_graph_samples*pt_spacing,plt_origin_y+40*y_scale),(255,255,255),1)
    cv2.line(resize,(plt_origin_x,plt_origin_y+20*y_scale),(plt_origin_x+fps_graph_samples*pt_spacing,plt_origin_y+20*y_scale),(255,255,255),1)
    cv2.putText(resize, text="FRAME-RATE (FPS)", org=(plt_origin_x+fps_graph_samples*pt_spacing -120,plt_origin_y-15),fontFace=cv2.	FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255,255,255), thickness=1)
    cv2.putText(resize, text="60", org=(plt_origin_x+fps_graph_samples*pt_spacing+10,plt_origin_y+5),fontFace=cv2.	FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255,255,255), thickness=1)
    cv2.putText(resize, text="40", org=(plt_origin_x+fps_graph_samples*pt_spacing+10,plt_origin_y+21*y_scale),fontFace=cv2.	FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255,255,255), thickness=1)
    cv2.putText(resize, text="20", org=(plt_origin_x+fps_graph_samples*pt_spacing+10,plt_origin_y+41*y_scale),fontFace=cv2.	FONT_HERSHEY_DUPLEX, fontScale=0.4, color=(255,255,255), thickness=1)
        # if key !=0:
            # cv2.line(resize,(plt_origin_x + key*pt_spacing - pt_gap, plt_origin_y- prev_ft*10),(plt_origin_x + key*pt_spacing, plt_origin_y-value*10),ft_color,1)


    # Calculate total time elapse since previous cv2.imshow, for PERFORMANCE ANALYSIS
    calc_time = (cv2.getTickCount() - before_showing)/ cv2.getTickFrequency()*1000
    if calc_time>16:
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # print calc_time
    # print "----"
      
    #vsync
    while ((cv2.getTickCount() - before_showing)/cv2.getTickFrequency()*10**6< 10**6/60.01):
        continue
    # print (cv2.getTickCount() - before_showing)/cv2.getTickFrequency()*1000 #check if equal 16.666, disable to ensure vsync works
    before_showing = cv2.getTickCount()
    cv2.imshow('frame',resize)


    prev_ret, prev_frame = ret, frame
    count = count + 1
    frametime = frametime + 1


    if pause_frame:
	    if cv2.waitKey(0) & 0xFF == ord('q'):
        	break
    else:    
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
        

cap.release()
cv2.destroyAllWindows()