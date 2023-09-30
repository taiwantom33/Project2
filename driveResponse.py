import picar_4wd as fc
import time

def response(com,speed):
	print(com)
	if com== b'87\r\n':
		fc.forward(speed)
		return (b'Forward',speed)
	elif com==b'83\r\n':
		fc.backward(speed)
		return (b'Backward',speed)
	elif com== b'65\r\n':
		fc.turn_left(speed)
		return (b'Left',speed)
	elif com== b'68\r\n':
		fc.turn_right(speed)
		return (b'Right',speed)
	elif com == b'Up\r\n':
		speed +=10
		return (b'SpeedingUp',speed)
	elif com== b'Down\r\n':
		speed -=10
		return (b'SlowingDown',speed)
	elif com == b'triggerOff\r\n':
		return (b'triggerOff',speed)
	elif com == b'triggerOn\r\n':
		return (b'triggerOn',speed)
	else:
		fc.forward(0)
		return (b'Stopping',speed)

def ultra_check():
    while True:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        if tmp != [2,2,2,2]:
            return 1
        else:
            return 0
	
