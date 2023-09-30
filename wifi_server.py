import socket
import driveResponse as dr
import multiprocessing
import subprocess

HOST = "192.168.0.103" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
speed=10

def get_cpu_temperature():
    try:
        result = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        temperature = float(result.replace("temp=", "").replace("'C\n", ""))
        return temperature
    except Exception as e:
        print("Error:", str(e))
        return None


danger = multiprocessing.Value('i',0)
dangerValues =["No Obstacle","Obstacle"]

def condition():
    while 1:
        danger.value = dr.ultra_check() 

condition_process = multiprocessing.Process(target=condition)
condition_process.start()
condition_process.terminate()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data==b'triggerOff\r\n':
                print("Off")
                condition_process.terminate()  
            cpu_temperature = get_cpu_temperature()
            if cpu_temperature is None:
                cpu_temp="Obtaining Temp"
            if data==b'triggerOn\r\n':
                print("On")
                condition_process.terminate()
                condition_process = multiprocessing.Process(target=condition)
                condition_process.start()
            if data != b"":
                print(data)
                (response,speed)=dr.response(data,speed)
                print(response)
                data_packet=response + b'|' + dangerValues[danger.value].encode('utf-8') + b'|' + str(speed).encode('utf-8') + b'|' + str(cpu_temperature).encode('utf-8') + b'\r\n'
                print(data_packet)
                client.sendall(data_packet) # Echo back to client
    except Exception as e: 
        print("Closing socket")
        print(e)
        client.close()
        s.close()
        condition_process.terminate()
        condition_process.join()    
