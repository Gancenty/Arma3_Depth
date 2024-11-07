import subprocess
import threading
import time
import numpy as np
import zmq

context1 = zmq.Context()
pub_socket = context1.socket(zmq.PUB)
pub_socket.bind("tcp://*:814")

context2 = zmq.Context()
sub_socket = context2.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:114")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")


def send_message(message):
    """
    ["agent.send_message", ["message"]] call py3_fnc_callExtension;
    """
    pub_socket.send_string(message)


def read_message():
    """
    ["agent.read_message", []] call py3_fnc_callExtension;
    """
    while True:
        try:
            message = sub_socket.recv(zmq.NOBLOCK)
            rec_data = np.frombuffer(message, dtype=np.float32)
            print(rec_data.shape)
            # rec_data.reshape(-1,2)
            # print(rec_data[0,:])
        except zmq.Again as e:
            pass


def start_threads():
    time.sleep(0.5)
    threads = []
    threads.append(
        threading.Thread(target=read_message, daemon=True)
    )
    for thread in threads:
        thread.start()
            


start_threads()
while True:
    # send_message(str([1,2,3]))
    time.sleep(1)