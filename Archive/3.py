import numpy as np
import cv2
from skimage.measure import compare_ssim




cap = cv2.VideoCapture("F:/ReLive/2020.09.18-09.20.mp4")

prev_frame = None

while(cap.isOpened()):
    ret, frame = cap.read()

    if not isinstance(prev_frame, list):
        prev_frame = frame

    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grey_frame, grey_prev_frame, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))






    cv2.imshow('frame',frame)


    prev_ret, prev_frame = ret, frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()