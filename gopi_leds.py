import requests

import os
import sys
import termios
import tty
import pigpio
import time
import datetime
import thread
#6, 15, 16, 18
RED_PIN   = 22
GREEN_PIN = 23
BLUE_PIN  = 24

RESPONSE_STATUS = "ERROR"

pi = pigpio.pi()

def checkStatus():
	global RESPONSE_STATUS
	START_TIME = time.time()
	CHECK_TIME = 0;
	sleep(10)
	while True:
		if (time.time() - START_TIME) > CHECK_TIME:
			response = requests.get("http://buildstatuscapone.herokuapp.com/status")
			RESPONSE_STATUS = response.text
			print "Response Recieved: ", RESPONSE_STATUS, "Current Time: ", time.strftime("%c")
			START_TIME = time.time()
			CHECK_TIME = 60

#sys.stdout = open("stdout.txt", "w")
def setLights(pin, brightness):
	#print "Pin: ", pin, " Brightness: ", brightness
	pi.set_PWM_dutycycle(pin, brightness)

def showBuildProgress():
	setLights(RED_PIN,0)
	setLights(BLUE_PIN,255)	
	setLights(GREEN_PIN,255)
	sleep(1)
	setLights(BLUE_PIN,0)
	sleep(1)
	setLights(BLUE_PIN,255)

def showBuildSuccess():
	setLights(GREEN_PIN, 255)
	setLights(BLUE_PIN, 0)
	setLights(RED_PIN, 0)
	sleep(15)		

def sleep(x):
	print "Sleeping for :", x, "Seconds. Current Time: ", time.strftime("%c")
	time.sleep(x)		

def showBuildFailure():
	setLights(GREEN_PIN, 0)
	setLights(BLUE_PIN, 0)
	setLights(RED_PIN, 255)
	sleep(15)		

def turnOff():
	setLights(RED_PIN,255)
	setLights(BLUE_PIN,255)	
	setLights(GREEN_PIN,255)
	sleep(1)
	setLights(GREEN_PIN,0)
	sleep(1)
	setLights(GREEN_PIN,255)
	
print "Initializing the request process"
thread.start_new_thread(checkStatus, ())

while True:
	print "USING RESPONSE_STATUS: ", RESPONSE_STATUS
	if RESPONSE_STATUS == '"IN_PROGRESS"':
		showBuildProgress()

	if RESPONSE_STATUS == '"SUCCESS"':
		showBuildSuccess()

	if RESPONSE_STATUS == '"FAIL"':
		showBuildFailure()

	if RESPONSE_STATUS == 'ERROR':
		turnOff()

	#time.sleep(1)
	print "END OF LOOP"
	#sys.stdout.flush()
