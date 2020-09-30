import numpy as np
import cv2
from skimage.measure import compare_ssim as ssim



cap = cv2.VideoCapture("F:/ReLive/2020.09.18-09.20.mp4")

prev_frame = None

while(cap.isOpened()):
    ret, frame = cap.read()

    if prev_frame == None:
    	prev_frame = frame

    simlarityIndex = ssim(frame, prev_frame)
    print simlarityIndex






    cv2.imshow('frame',frame)


    prev_ret, prev_frame = ret, frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()