import queue
import random

frames_q = queue.Queue(maxsize=6)

def add_to_queue(frame, type):
    global frames_q
    if frames_q.full():
        frames_q.get()
    frames_q.put({"frame" : frame, "type" : type})

def queue_max():
    global frames_q
    counters = {"front" : 0, "left" : 0, "right" : 0, "total" : 0}
    for frame_info in list(frames_q.queue):
        counters[frame_info["type"]] += 1
        counters["total"] += 1
    for key in counters.keys():
        counters[key] = counters[key]/counters['total'] * 100
    counters['total'] = 0
    maximum = max(counters.values())
    if maximum > 34:
        return list(counters.keys())[list(counters.values()).index(maximum)]
    return "no candidate"
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