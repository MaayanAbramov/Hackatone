import math
import os
import time
from asyncio.windows_events import NULL

import cv2
import numpy as np
from gtts import gTTS
from playsound import playsound

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
gTTS(text="Please adjust your face my man", lang="en").save("lostFace.mp3")
gTTS(text="Please turn right my man", lang="en").save("adjustEyesRight.mp3")
gTTS(text="Please turn left my man", lang="en").save("adjustEyesLeft.mp3")

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    width = int(cap.get(3))
    height = int(cap.get(4))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    scaleFactor=1.2
    minNeighbors=5
    lineThickness=3
    green=(0, 255, 0)
    blue=(255, 0, 0)
    red=(0, 0, 255)
    faces = face_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)
    """
    if len(faces) == 0:
        playsound('lostFace.mp3')
        time.sleep(0.2)
    """
    for (x, y, w, h) in faces:
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
            if len(eyes)==1:
                if eyeCenterXAxis > faceCenterXAxis:
                    playsound('adjustEyesRight.mp3')
                    time.sleep(0.1)
                elif eyeCenterXAxis < faceCenterXAxis:
                    playsound('adjustEyesLeft.mp3')
                    time.sleep(0.1)
            """
            if len(eyes) == 0:
                playsound('lostEyes.mp3')
                time.sleep(0.2)
            """
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
