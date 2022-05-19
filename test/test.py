import math
import os
import time
import multiprocessing

import cv2
import numpy as np
from gtts import gTTS
from playsound import playsound

play_audio_last = 0.0
epsilon = 1.0

cap = cv2.VideoCapture(0)
profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

"""
gTTS(text="Welcome my man", lang="en").save("Welcome.mp3")
gTTS(text="Please adjust your face my man", lang="en").save("lostFace.mp3")
gTTS(text="Please turn right my man", lang="en").save("adjustEyesRight.mp3")
gTTS(text="Please turn left my man", lang="en").save("adjustEyesLeft.mp3")
"""
p = multiprocessing.Process()

def play_audio(audio_file):
    #global p
    global play_audio_last
    current_t = time.time()
    if current_t - play_audio_last > 2:
    #if not p.is_alive():
        #p = multiprocessing.Process(target=playsound(audio_file, block = False))
        #p.start()
        playsound(audio_file, block = False)
        play_audio_last = time.time()

def main():
    frame_cout = 0
    frame_spree_type = 0
    while True:
        ret, frame = cap.read()
        frame_fliped = frame
        frame = cv2.flip(frame, 1)
        width = int(cap.get(3))
        height = int(cap.get(4))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_fliped = cv2.cvtColor(frame_fliped, cv2.COLOR_BGR2GRAY)
        scaleFactor=1.2
        minNeighbors=5
        lineThickness=3
        green=(0, 255, 0)
        blue=(255, 0, 0)
        blue_green=(255,255,0)
        blue_red=(255,0,255)
        red=(0, 0, 255)
        faces = face_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)
        right_profile_cascade = profile_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)
        left_profile_cascade = profile_cascade.detectMultiScale(gray_fliped, scaleFactor, minNeighbors)
        if len(faces) == 0:
            if len(right_profile_cascade) != 0:
                if(frame_cout < 30):
                    if frame_spree_type == 1:
                        frame_cout+=1
                    else:
                        frame_cout = 1
                        frame_spree_type = 1
                else:
                    play_audio('adjustEyesRight.mp3')
                    frame_cout = 1
            elif len(left_profile_cascade) != 0:
                if(frame_cout < 30):
                    if frame_spree_type == 2:
                        frame_cout+=1
                    else:
                        frame_cout = 1
                        frame_spree_type = 2
                else:
                    play_audio('adjustEyesLeft.mp3')
                    frame_cout = 1
            else:
                if(frame_cout < 30):
                    if frame_spree_type == 3:
                        frame_cout+=1
                    else:
                        frame_cout = 1
                        frame_spree_type = 3
                else:
                    play_audio('lostFace.mp3')
                    frame_cout = 1
        profile_side_faceMaxX=0
        profile_side_faceMaxY=0
        profile_side_faceMaxW=0
        profile_side_faceMaxH=0
        for(x, y, w, h) in right_profile_cascade:
            if (w*h)>(profile_side_faceMaxW)*(profile_side_faceMaxH):
                profile_side_faceMaxX=x
                profile_side_faceMaxY=y
                profile_side_faceMaxW=w
                profile_side_faceMaxH=h
            #play_audio('adjustEyesRight.mp3')
            #cv2.rectangle(frame, (x, y), (x + w, y + h), blue_green, lineThickness)
        profile_side_leftMaxX=0
        profile_side_leftMaxY=0
        profile_side_leftMaxW=0
        profile_side_leftMaxH=0
        for(x, y, w, h) in left_profile_cascade:
            if (w*h)>(profile_side_leftMaxW*profile_side_leftMaxH):
                profile_side_leftMaxX=x
                profile_side_leftMaxY=y
                profile_side_leftMaxW=w
                profile_side_leftMaxH=h
            #play_audio('adjustEyesLeft.mp3')
            #cv2.rectangle(frame, (width-x, y), (width-(x + w), y + h), blue_red, lineThickness)
        faceMaxX=0
        faceMaxY=0
        faceMaxW=0
        faceMaxH=0
        for (x, y, w, h) in faces:
            #t0 = time.clock()
            #if len(faces) == 0:# and not p.is_alive():
                #p = multiprocessing.Process(target=playsound, args='lostFace.mp3').start()
                #play_audio('lostFace.mp3')
                #time.sleep(0.2)
            if (w*h)>(faceMaxW*faceMaxH):
                faceMaxX=x
                faceMaxY=y
                faceMaxW=w
                faceMaxH=h
            #cv2.rectangle(frame, (x, y), (x + w, y + h), blue, lineThickness)
            faceCenterXAxis=x+w//2
            roi_gray = gray[y:y+w, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor, minNeighbors)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), green, lineThickness)
                eyeCenterXAxis=x+ex+ew//2
                eyeCenterYAxis=y+ey+eh//2
                cv2.line(frame, (eyeCenterXAxis, 0), (eyeCenterXAxis, height), red, lineThickness)
                cv2.line(frame, (0, eyeCenterYAxis), (width, eyeCenterYAxis), red, lineThickness)
                """
                if len(eyes)==1:
                    if eyeCenterXAxis > faceCenterXAxis:
                        play_audio('adjustEyesRight.mp3')
                    elif eyeCenterXAxis < faceCenterXAxis:
                        play_audio('adjustEyesLeft.mp3')
                """
        #cv2.rectangle(frame, (faceMaxX, faceMaxY), (faceMaxX + faceMaxW, faceMaxY + faceMaxH), blue, lineThickness)
        #cv2.rectangle(frame, (profile_side_faceMaxX, profile_side_faceMaxY), (profile_side_faceMaxX + profile_side_faceMaxW, profile_side_faceMaxY + profile_side_faceMaxH), blue_green, lineThickness)
        if (profile_side_faceMaxW*profile_side_faceMaxH)>(faceMaxW*faceMaxH) and (profile_side_faceMaxW*profile_side_faceMaxH) > (profile_side_leftMaxW*profile_side_leftMaxH):
            MaxX=profile_side_faceMaxX
            MaxY=profile_side_faceMaxY
            MaxW=profile_side_faceMaxW
            MaxH=profile_side_faceMaxH
            color=blue_green
        elif (profile_side_leftMaxW*profile_side_leftMaxH > (profile_side_faceMaxW*profile_side_faceMaxH) and (profile_side_leftMaxW*profile_side_leftMaxH) > (faceMaxW*faceMaxH)):
            MaxX=width-profile_side_leftMaxX-profile_side_leftMaxW
            MaxY=profile_side_leftMaxY
            MaxW=profile_side_leftMaxW
            MaxH=profile_side_leftMaxH
            color=blue_red
        else:
            MaxX=faceMaxX
            MaxY=faceMaxY
            MaxW=faceMaxW
            MaxH=faceMaxH
            color=blue
        cv2.rectangle(frame, (MaxX, MaxY), (MaxX + MaxW, MaxY + MaxH), color, lineThickness)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    """
    if os.path.exists("Welcome.mp3"):
        os.remove("Welcome.mp3")
    if os.path.exists("lostFace.mp3"):
        os.remove("lostFace.mp3")
    if os.path.exists("adjustEyesRight.mp3"):
        os.remove("adjustEyesRight.mp3")
    if os.path.exists("adjustEyesLeft.mp3"):
        os.remove("adjustEyesLeft.mp3")
    """

if __name__ == "__main__":
    main()
