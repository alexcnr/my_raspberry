import RPi.GPIO as GPIO 
import time

#GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)



for i in range(10): 
    GPIO.output(12,True)
    time.sleep(0.5)
    GPIO.output(12,False)
    time.sleep(0.5)
    
GPIO.cleanup()
print("Мигания закончились!")
