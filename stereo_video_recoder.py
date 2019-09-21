import numpy as np
import cv2
from datetime import datetime
import os
import time
import math

"""
CONFIG
"""
CAMERA_DEVISE_L = 0
CAMERA_DEVISE_R = 2

IMAGE_WIDTH = 320
IMAGE_HEIGHT = 240

SAVED_FOLDER = 'videos'

PREFERED_FRAME_RATE = 15
"""
"""

if not os.path.exists(SAVED_FOLDER):
    os.mkdir(SAVED_FOLDER)


capl = cv2.VideoCapture(CAMERA_DEVISE_L)
capl.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
capl.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)

capr = cv2.VideoCapture(CAMERA_DEVISE_R)
capr.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
capr.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)


is_recording = False
recl = None
recr = None
frame_rate = 0
last_update_time = time.time()
pathl = ''
pathr = ''

lbuttonup = False
mbuttonup = False
def mouse_event(event, x, y, flags, param):
    global lbuttonup, mbuttonup
    
    if event == cv2.EVENT_MBUTTONUP:
        mbuttonup = True
    elif event == cv2.EVENT_LBUTTONUP:
        lbuttonup = True


cv2.namedWindow("screen", cv2.WINDOW_NORMAL)
cv2.setWindowProperty('screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback("screen", mouse_event)

while True:

    if not (capl.grab() and capr.grab()):
        print("No more frames")
        break

    ret, framel = capl.read()
    ret, framer = capr.read()

    if is_recording:
        if recl is not None:
            recl.write(framel)
        if recr is not None:
            recr.write(framer)

    # 画面に表示する
    screen = cv2.hconcat([framel, framer])
    if is_recording and math.sin(2.0 * math.pi * time.time() / 2.0) > -0.75:
        screen = cv2.circle(screen,(10,10), 8, (0,0,255), -1)
        cv2.putText(screen, 'REC', (20, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), thickness=2)
    
    cv2.imshow('screen', screen)

    frame_rate = min(int((1.0 / (time.time() - last_update_time)) * 2.0 + frame_rate) / 3.0, PREFERED_FRAME_RATE)

    if frame_rate < PREFERED_FRAME_RATE:
        print('[WARNING] frame rate is lower than preferd one. now frame_rate: ', frame_rate)

    wait_time = 1
    if(frame_rate != 0.0):
        wait_time = int((1.0 / frame_rate - (time.time() - last_update_time)) * 1000)
    # print(wait_time)
    if(wait_time <= 0):
        wait_time = 1
    key = cv2.waitKey(wait_time) & 0xFF
    # q or esc が押された場合は終了する
    if key == ord('q') or key == 27 or mbuttonup:
        break

    if key == ord('r') or lbuttonup:
        if is_recording:
            recl.release()
            recr.release()
            recl = None
            recr = None
            print("[NOTE] Save file. {}".format(pathl))
            print("[NOTE] Save file. {}".format(pathr))
            is_recording = False
        else:
            print("[NOTE] Start Recording!")
            
            filename_base = datetime.now().strftime("%Y%m%d-%H%M%S")
            pathl = SAVED_FOLDER + '/' + filename_base + "-Left.avi"
            pathr = SAVED_FOLDER + '/' + filename_base + "-Right.avi"
            
            recl = cv2.VideoWriter(pathl,
                                  cv2.VideoWriter_fourcc(*'mp4v'),
                                  frame_rate,
                                  (IMAGE_WIDTH, IMAGE_HEIGHT), True)

            recr = cv2.VideoWriter(pathr,
                                  cv2.VideoWriter_fourcc(*'mp4v'),
                                  frame_rate,
                                  (IMAGE_WIDTH, IMAGE_HEIGHT), True)
            is_recording = True
    
    lbuttonup = False
    mbuttonup = False
    last_update_time = time.time()
    
# キャプチャの後始末と，ウィンドウをすべて消す

if is_recording:
    recl.release()
    recr.release()
    print("[NOTE] Save file. {}".format(pathl))
    print("[NOTE] Save file. {}".format(pathr))

capl.release()
capr.release()
cv2.destroyAllWindows()