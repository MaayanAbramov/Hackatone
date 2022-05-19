import queue
import random

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


def is_static(face, frame, percentage):
    global frames_q
    static_frames_counter = 0
    epsilon = 3
    for frame_info in list(frames_q.queue):
        if (frame_info["frame"][face[0]:face[0]+face[2]][face[1]:face[1]+face[3]] <= frame[face[0]:face[0]+face[2]][face[1]:face[1]+face[3]] + epsilon) or (frame_info["frame"][face[0]:face[0]+face[2]][face[1]:face[1]+face[3]] >= frame[face[0]:face[0]+face[2]][face[1]:face[1]+face[3]] - epsilon) :
            static_frames_counter += 1
    if static_frames_counter/max(frames_q.qsize(),1)*100 > percentage:
        return True
    return False

'''
def main():
    global frames_q
    stuff= ("left", "right" ,"right" , "left", "front", "front")
    for i in range(6):
        add_to_queue( 0 ,stuff[i] )
    print(queue_max())
    

if __name__ == "__main__":
    main()
'''
