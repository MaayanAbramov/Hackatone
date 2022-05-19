from email.mime import audio
import math
import os
import time
import multiprocessing
from asyncio.windows_events import NULL
from types import NoneType

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
    global p
    #global play_audio_last
    #current_t = time.time()
    #if current_t - play_audio_last > 2:
    if not p.is_alive():
        p = multiprocessing.Process(target=playsound(audio_file, block = False))
        p.start()
        #playsound(audio_file, block = False)
        #play_audio_last = time.time()

def main():
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
        for(x, y, w, h) in right_profile_cascade:
            play_audio('adjustEyesRight.mp3')
            cv2.rectangle(frame, (x, y), (x + w, y + h), blue_green, lineThickness)
        for(x, y, w, h) in left_profile_cascade:
            play_audio('adjustEyesLeft.mp3')
            cv2.rectangle(frame, (x, y), (x + w, y + h), blue_red, lineThickness)
        for (x, y, w, h) in faces:
            #t0 = time.clock()
            if len(faces) == 0:# and not p.is_alive():
                #p = multiprocessing.Process(target=playsound, args='lostFace.mp3').start()
                play_audio('lostFace.mp3')
                #time.sleep(0.2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), blue, lineThickness)
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
