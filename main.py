import cv2
import mediapipe as mp
import math
import numpy as np
from fontTools.misc.cython import returns
from google.protobuf.json_format import MessageToDict
from math import hypot
from brightnes_lefthand import Brightness #for Brightness control
#for volume control
from volume_control_righthand import Volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volbar=400
volper=0
volMin,volMax=volume.GetVolumeRange()[:2]

mphands=mp.solutions.hands
hands=mphands.Hands(static_image_mode=False,
                    model_complexity=1
                    ,max_num_hands=2,
                    min_detection_confidence=0.75,
                    min_tracking_confidence=0.5)
Draw=mp.solutions.drawing_utils
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img=cv2.flip(img,1)
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    if results.multi_hand_landmarks:
        if len(results.multi_handedness)==2:
            cv2.putText(img,'bothhands',
                        (250,50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (0,255,0),
                        2
                        )
            cv2.imshow('img',img)
        else:
            for i in results.multi_handedness:
                label=MessageToDict(i)['classification'][0]['label']
                if label=='Left':
                    cv2.putText(img,label+'hand',(10,50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                1,(0,255,255),
                                2)
                    Brightness(img,imgRGB,results,Draw,mphands,hands)
                    cv2.imshow('img',img)
                if label=='Right':
                    cv2.putText(img,label+'hand',(460,50),
                                cv2.FONT_HERSHEY_COMPLEX,
                                1,(0,255,0),2)
                    Volume(img,imgRGB,results,Draw,mphands,hands)
                    cv2.imshow('img',img)

    # cv2.imshow("image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()