import math
import multiprocessing
import os
import time

import cv2
import numpy
from gtts import gTTS
from playsound import playsound

play_audio_last = 0.0
epsilon = 1.0

X_INDEX=0
Y_INDEX=1
W_INDEX=2
H_INDEX=3

audio_names=("lostFace.mp3", "adjustEyesRight.mp3", "adjustEyesLeft.mp3")

def delete_audio():
    for(audio) in audio_names:
        if os.path.exists(audio):
            os.remove(audio)

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
    cap = cv2.VideoCapture(0)
    profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    delete_audio()

    gTTS(text="Please adjust your face", lang="en").save("lostFace.mp3")
    gTTS(text="Please look right", lang="en").save("adjustEyesRight.mp3")
    gTTS(text="Please look left", lang="en").save("adjustEyesLeft.mp3")

    p = multiprocessing.Process()

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
        profile_side_rightMax=(0,0,0,0)
        for(x, y, w, h) in right_profile_cascade:
            if (w*h)>(profile_side_rightMax[W_INDEX])*(profile_side_rightMax[H_INDEX]):
                profile_side_rightMax=(x, y, w, h)
            #play_audio('adjustEyesRight.mp3')
            #cv2.rectangle(frame, (x, y), (x + w, y + h), blue_green, lineThickness)
        profile_side_leftMax=(0,0,0,0)
        for(x, y, w, h) in left_profile_cascade:
            if (w*h)>(profile_side_leftMax[W_INDEX]*profile_side_leftMax[H_INDEX]):
                profile_side_leftMax=(x, y, w, h)
            #play_audio('adjustEyesLeft.mp3')
            #cv2.rectangle(frame, (width-x, y), (width-(x + w), y + h), blue_red, lineThickness)
        faceMax=(0,0,0,0)
        for (x, y, w, h) in faces:
            #t0 = time.clock()
            #if len(faces) == 0:# and not p.is_alive():
                #p = multiprocessing.Process(target=playsound, args='lostFace.mp3').start()
                #play_audio('lostFace.mp3')
                #time.sleep(0.2)
            if (w*h)>(faceMax[W_INDEX]*faceMax[H_INDEX]):
                faceMax=(x, y, w, h)
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
        if (profile_side_rightMax[W_INDEX]*profile_side_rightMax[H_INDEX])>(faceMax[W_INDEX]*faceMax[H_INDEX]) and (profile_side_rightMax[W_INDEX]*profile_side_rightMax[H_INDEX]) > (profile_side_leftMax[W_INDEX]*profile_side_leftMax[H_INDEX]):
            Max=profile_side_rightMax
            color=blue_green
        elif (profile_side_leftMax[W_INDEX]*profile_side_leftMax[H_INDEX] > (profile_side_rightMax[W_INDEX]*profile_side_rightMax[H_INDEX]) and (profile_side_leftMax[W_INDEX]*profile_side_leftMax[H_INDEX]) > (faceMax[W_INDEX]*faceMax[H_INDEX])):
            Max=profile_side_leftMax
            tempMax=list(Max)
            tempMax[X_INDEX]=width-profile_side_leftMax[X_INDEX]-profile_side_leftMax[W_INDEX]
            Max=tuple(tempMax)
            color=blue_red
        else:
            Max=faceMax
            color=blue
        cv2.rectangle(frame, (Max[X_INDEX], Max[Y_INDEX]), (Max[X_INDEX] + Max[W_INDEX], Max[Y_INDEX] + Max[H_INDEX]), color, lineThickness)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    delete_audio()

if __name__ == "__main__":
    main()
