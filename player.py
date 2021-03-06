import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import os
import subprocess
from subprocess import call

# Start the video playback in the background
subprocess.Popen(["omxplayer", "/media/pi/44C0-AEBF/Casto.S01E01.mp4", "< /tmp/cmd"])

TRIG = 20                                  #Associate pin 23 to TRIG
ECHO = 26                                  #Associate pin 24 to ECHO

print "Setup in progress"

started = None

try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering
    GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in
    GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out

    print "Distance measurement in progress"

    while True:

        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        time.sleep(0.05)                         #Delay of 2 seconds

        GPIO.output(TRIG, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(TRIG, False)                 #Set TRIG as LOW

        while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
            pulse_start = time.time()              #Saves the last known time of LOW pulse

        while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
            pulse_end = time.time()                #Saves the last known time of HIGH pulse

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)            #Round to two decimal points

#        print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration

        if distance < 60:
            if started == None:
                subprocess.Popen(["echo",".",">","/tmp/cmd"])
                started = True

        elif distance > 100 and distance < 200:
            if started == True:
                subprocess.Popen(["echo","-n","p",">","/tmp/cmd"])
                started = None


except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    call(["killall","omxplayer"])
