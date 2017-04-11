import requests

import os
import sys
import termios
import tty
import pigpio
import time
import datetime

RED_PIN   = 22
GREEN_PIN = 23
BLUE_PIN  = 24

sys.stdout = open("stdout.txt", "w")
def setLights(pin, brightness):
	#text_file.write("PIN %s %s" % pin % brightness)
	pi.set_PWM_dutycycle(pin, brightness)

def blinkGreen():
	for x in range (0, 255):
		time.sleep(0.02)
		setLights(GREEN_PIN, 255)
		time.sleep(0.5)
		setLights(GREEN_PIN, 0)
	
def blinkBlue():
	setLights(GREEN_PIN, 0)
	setLights(RED_PIN, 0)
	setLights(BLUE_PIN, 255)


def blinkRed():
	setLights(GREEN_PIN, 0)
	setLights(RED_PIN, 255)
	setLights(BLUE_PIN, 0)


def turnOff():
	setLights(GREEN_PIN,0)
	setLights(RED_PIN,0)
	setLights(BLUE_PIN,0)

while True:

	response = requests.get("http://buildstatuscapone.herokuapp.com/status")
	pi = pigpio.pi()
	print 
        print(" %s -- %s  " % (response.text, datetime.datetime.now()))

        sys.stdout.flush()
	if response.text == '"IN_PROGRESS"':
		
		print "HEY, IN_PROGRESS"

		for i in range(0,3):

			for i in range(0,5):
				for i in range(0,101):
					setLights(BLUE_PIN, i)
					setLights(GREEN_PIN, i)	
					time.sleep(0.002)

				for i in range(100,-1, -1):
					setLights(GREEN_PIN, i)
					setLights(BLUE_PIN, i)	
					time.sleep(0.002)
				time.sleep(1)

				
			print "IN_PROGRESS"
			
	
	if response.text == '"SUCCESS"':
		print "HEY, SUCCESS"
		
		setLights(GREEN_PIN, 255)
		setLights(RED_PIN, 0)
		setLights(BLUE_PIN, 255)
		time.sleep(10)
		print "SUCCESS"

	if response.text == '"FAIL"':
		print "HEY, FAILED"
		turnOff()
		for i in range(0,5):

			setLights(RED_PIN, 255)
			setLights(GREEN_PIN, 100)
			time.sleep(3)
			
			for a in range(100,-1, -1):
				setLights(RED_PIN, a)
				setLights(GREEN_PIN, i)	
				time.sleep(0.01)

			print "FAILED"
			time.sleep(0.3)

	print "END OF LOOP"

