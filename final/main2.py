import os
import time

import cv2
import function
from gtts import gTTS
from playsound import playsound

LAST_AUDIO_PLAYED = 0.0
AUDIO_PLAY_PAUSE = 5.0

GREEN=(0, 255, 0)
BLUE=(255, 0, 0)
BLUE_GREEN=(255,255,0)
BLUE_RED=(255,0,255)
RED=(0, 0, 255)

X_INDEX=0
Y_INDEX=1
W_INDEX=2
H_INDEX=3

audio_names=("lostFace.mp3", "adjustEyesRight.mp3", "adjustEyesLeft.mp3")

def findMax(frame, width, faces, right_profile_cascade, left_profile_cascade):
        profile_side_rightMax=(0,0,0,0)
        for(x, y, w, h) in right_profile_cascade:
            #if function.is_static((x, y, w, h), frame, 90):
                #continue
            if (w*h)>(profile_side_rightMax[W_INDEX])*(profile_side_rightMax[H_INDEX]):
                profile_side_rightMax=(x, y, w, h)
        profile_side_leftMax=(0,0,0,0)
        for(x, y, w, h) in left_profile_cascade:
            #if function.is_static((width-x-w, y, w, h), frame, 90):
                #continue
            if (w*h)>(profile_side_leftMax[W_INDEX]*profile_side_leftMax[H_INDEX]):
                profile_side_leftMax=(x, y, w, h)
        faceMax=(0,0,0,0)
        for (x, y, w, h) in faces:
            #if function.is_static((x, y, w, h), frame, 90):
                #continue
            if (w*h)>(faceMax[W_INDEX]*faceMax[H_INDEX]):
                faceMax=(x, y, w, h)
        Max=(0, 0, 0, 0)
        if (profile_side_rightMax[W_INDEX]*profile_side_rightMax[H_INDEX])>(faceMax[W_INDEX]*faceMax[H_INDEX]) and (profile_side_rightMax[W_INDEX]*profile_side_rightMax[H_INDEX]) > (profile_side_leftMax[W_INDEX]*profile_side_leftMax[H_INDEX]):
            Max=profile_side_rightMax
            color=BLUE_GREEN
            function.add_to_queue(frame, "right")
        elif (profile_side_leftMax[W_INDEX]*profile_side_leftMax[H_INDEX] > (profile_side_rightMax[W_INDEX]*profile_side_rightMax[H_INDEX]) and (profile_side_leftMax[W_INDEX]*profile_side_leftMax[H_INDEX]) >= (faceMax[W_INDEX]*faceMax[H_INDEX])):
            Max=profile_side_leftMax
            tempMax=list(Max)
            tempMax[X_INDEX]=width-profile_side_leftMax[X_INDEX]-profile_side_leftMax[W_INDEX]
            Max=tuple(tempMax)
            color=BLUE_RED
            function.add_to_queue(frame, "left")
        elif (faceMax[W_INDEX]*faceMax[H_INDEX] > (profile_side_rightMax[W_INDEX]*profile_side_rightMax[H_INDEX]) and (faceMax[W_INDEX]*faceMax[H_INDEX]) > (profile_side_leftMax[W_INDEX]*profile_side_leftMax[H_INDEX])):
            Max=faceMax
            color=BLUE
            function.add_to_queue(frame, "front")
        else:
            function.add_to_queue(frame, "none")
            color = (0,0,0)
        return (Max, color)

def create_audio():
    gTTS(text="Please adjust your face", lang="en").save("lostFace.mp3")
    gTTS(text="Please look right", lang="en").save("adjustEyesRight.mp3")
    gTTS(text="Please look left", lang="en").save("adjustEyesLeft.mp3")

def delete_audio():
    for(audio) in audio_names:
        if os.path.exists(audio):
            os.remove(audio)

def play_audio(audio_file):
    global LAST_AUDIO_PLAYED
    current_t = time.time()
    if current_t - LAST_AUDIO_PLAYED > AUDIO_PLAY_PAUSE:
        playsound(audio_file, block = False)
        LAST_AUDIO_PLAYED = time.time()

def main():
    cap = cv2.VideoCapture(0)
    profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    delete_audio()
    create_audio()

    frame_cout = 0
    frame_spree_type = 0
    scaleFactor=1.2
    minNeighbors=5
    lineThickness=3

    while True:
        ret, frame = cap.read()
        frame_fliped = frame
        frame = cv2.flip(frame, 1)
        width = int(cap.get(3))
        height = int(cap.get(4))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_fliped = cv2.cvtColor(frame_fliped, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)
        right_profile_cascade = profile_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)
        left_profile_cascade = profile_cascade.detectMultiScale(gray_fliped, scaleFactor, minNeighbors)
        (Max, color) = findMax(frame, width, faces, right_profile_cascade, left_profile_cascade)
        cv2.rectangle(frame, (Max[X_INDEX], Max[Y_INDEX]), (Max[X_INDEX] + Max[W_INDEX], Max[Y_INDEX] + Max[H_INDEX]), color, lineThickness)
        match function.queue_max(34) :
            case "right" : 
                play_audio('adjustEyesRight.mp3')
            case "left" :
                play_audio('adjustEyesLeft.mp3')
            case "none" :
                play_audio('lostFace.mp3') 
        

        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    delete_audio()

if __name__ == "__main__":
    main()
