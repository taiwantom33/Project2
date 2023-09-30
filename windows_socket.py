import socket
import threading
from collections import deque
import signal
import time

server_addr = 'D8:3A:DD:1F:98:30'
server_port = 1

buf_size = 1024

client_sock = None
server_sock = None
sock = None

exit_event = threading.Event()

message_queue = deque([])
output = ""

dq_lock = threading.Lock()
output_lock = threading.Lock()

def handler(signum, frame):
    exit_event.set()


signal.signal(signal.SIGINT, handler)

def start_client():
    global sock
    global dq_lock
    global output_lock
    global exit_event
    global message_queue
    global output
    global server_addr
    global server_port
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.settimeout(10)
    sock.connect((server_addr,server_port))
    sock.settimeout(None)
    print("after connect")
    sock.setblocking(False)
    while not exit_event.is_set():
        if dq_lock.acquire(blocking=False):
            if(len(message_queue) > 0):
                try:
                    sent = sock.send(bytes(message_queue[0], 'utf-8'))
                except Exception as e:
                    exit_event.set()
                    continue
                if sent < len(message_queue[0]):
                    message_queue[0] = message_queue[0][sent:]
                else:
                    message_queue.popleft()
            dq_lock.release()
        
        if output_lock.acquire(blocking=False):
            data = ""
            try:
                try:
                    data = sock.recv(1024).decode("utf-8")
                except socket.error as e:
                    assert(1==1)
                    #no data
            except Exception as e:
                exit_event.set()
                continue
            output += data
            output_split = output.split("\r\n")
            for i in range(len(output_split) - 1):
                print(output_split[i])
            output = output_split[-1]
            output_lock.release()
    sock.close()
    print("client thread end")


cth = threading.Thread(target=start_client)

cth.start()


print("finish join")
j = 0
while not exit_event.is_set():
    dq_lock.acquire()
    message_queue.append("PC " + str(j) + " \r\n")
    dq_lock.release()
    j += 1
    time.sleep(2)

print("Disconnected.")



print("All done.")
