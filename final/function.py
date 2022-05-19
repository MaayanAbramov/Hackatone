import queue

import numpy as np

frames_q = queue.Queue(maxsize=6)

def add_to_queue(frame, _type):
    global frames_q
    if frames_q.full():
        frames_q.get()
    frames_q.put({"frame": frame, "type": _type})

def queue_max(percentage):
    global frames_q
    counters = {"front": 0, "left": 0, "right": 0, "none": 0, "total": 0}
    for frame_info in list(frames_q.queue):
        counters[frame_info["type"]] += 1
        counters["total"] += 1
    for key in counters.keys():
        counters[key] = counters[key] / counters['total'] * 100
    counters['total'] = 0
    maximum = max(counters.values())
    if maximum > percentage:
        return list(counters.keys())[list(counters.values()).index(maximum)]
    return "no candidate"

def mse (image1, image2) :
    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
    err /= float(image1.shape[0] * image1.shape[1])
    return err #the lower - the better

def is_static(face, frame, percentage):
    global frames_q
    static_frames_counter = 0
    epsilon = 3
    for frame_info in list(frames_q.queue):
        flag = False
        #for i in range(face[2]):
            #for j in range(face[3]):
                #for k in range(3):
                    #if frame_info["frame"][face[0] + i][face[2] + j][k] == frame[face[0] + i][face[2] + j][k]:
                        #flag = True
        if(mse(frame_info["frame"][face[0]:face[0]+face[2]][face[1]:face[1]+face[3]],frame[face[0]:face[0]+face[2]][face[1]:face[1]+face[3]]) < 0.8):
        #if (frame_info["frame"][face[0]:face[0]+face[2]][face[1]:face[1]+face[3]] == frame[face[0]:face[0]+face[2]][face[1]:face[1]+face[3]] + epsilon) or (frame_info["frame"][face[0]:face[0]+face[2]][face[1]:face[1]+face[3]] >= frame[face[0]:face[0]+face[2]][face[1]:face[1]+face[3]] - epsilon) :
        #if(flag):
            static_frames_counter += 1
    if static_frames_counter/max(frames_q.qsize(),1)*100 > percentage:
        return True
    return False