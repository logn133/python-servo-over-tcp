import RPi.GPIO as GPIO
import string
import socket
import time
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addrs = ('192.168.1.231', 420)
print >>sys.stderr, 'starting up on %s port %s' % server_addrs
sock.bind(server_addrs)
sock.listen(1)

pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)
off = 12.5
on = 5

def SetAngle(angle):
    duty = angle/18+2
    GPIO.output(pin, True)
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(pin, False)
    p.ChangeDutyCycle(0)
    print (angle)


while True:
    print >>sys.stderr, 'waiting for connection'
    connection, client_addrs = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_addrs

        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'recieved "%s"' % data
            if data:
                print >>sys.stderr, 'sending confirmation to the client'
                SetAngle(int(data))                
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_addrs
                break

    finally:
        connection.close()
        p.stop()
        GPIO.cleanup()

