import requests

import os
import sys
import termios
import tty
import pigpio
import time
import datetime
import thread

RED_PIN   = 22
GREEN_PIN = 23
BLUE_PIN  = 24

RESPONSE_STATUS = "ERROR"

pi = pigpio.pi()

def checkStatus():
	global RESPONSE_STATUS
	START_TIME = time.time()
	CHECK_TIME = 0;
	time.sleep(5)
	while True:
		if (time.time() - START_TIME) > CHECK_TIME:
			response = requests.get("http://buildstatuscapone.herokuapp.com/status")
			RESPONSE_STATUS = response.text
			print "Response Recieved: ", RESPONSE_STATUS, "Current Time: ", (time.time())
			START_TIME = time.time()
			CHECK_TIME = 60

sys.stdout = open("stdout.txt", "w")
def setLights(pin, brightness):
	text_file.write("PIN %s %s" % pin % brightness)
	print "Pin: ", pin, " Brightness: ", brightness
	pi.set_PWM_dutycycle(pin, brightness)

def showBuildProgress():
	for x in range (0, 255):
		time.sleep(0.1)
		setLights(GREEN_PIN, x)
		setLights(BLUE_PIN, x)
		setLights(RED_PIN, 0)
		print "Showing IN_PROGRESS with brightness", x
	for x in range (255, 1, -1):
		time.sleep(0.1)
		setLights(GREEN_PIN, x)
		setLights(BLUE_PIN, x)
		setLights(RED_PIN, 0)
		print "Showing IN_PROGRESS with brightness", x


def showBuildSuccess():
	setLights(GREEN_PIN, 255)
	setLights(BLUE_PIN, 255)
	setLights(RED_PIN, 255)

def showBuildFailure():
	for x in range (0, 255):
		time.sleep(0.2)
		setLights(GREEN_PIN, 0)
		setLights(BLUE_PIN, x)
		setLights(RED_PIN, x)
		print "Showing FAIL with brightness", x
	for x in range (255, 1, -1):
		time.sleep(0.2)
		setLights(GREEN_PIN, 0)
		setLights(BLUE_PIN, x)
		setLights(RED_PIN, x)
		print "Showing FAIL with brightness", x

def turnOff():
	setLights(GREEN_PIN,0)
	setLights(RED_PIN,0)
	setLights(BLUE_PIN,0)


print "Initializing the request process"
thread.start_new_thread(checkStatus, ())

while True:
	print "RESPONSE_STATUS: ", RESPONSE_STATUS
	if RESPONSE_STATUS == '"IN_PROGRESS"':
		print "HEY, IN_PROGRESS"
		showBuildProgress()

	if RESPONSE_STATUS == '"SUCCESS"':
		print "HEY, SUCCESS"
		showBuildSuccess()

	if RESPONSE_STATUS == '"FAIL"':
		print "HEY, FAILED"
		turnOff()
		showBuildFailure()

	if RESPONSE_STATUS == 'ERROR':
		print "NO RESPONSE, YET"
		turnOff()

	time.sleep(10)
	print "END OF LOOP"
	sys.stdout.flush()
