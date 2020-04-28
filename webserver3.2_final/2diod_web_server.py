
import RPi.GPIO as GPIO 
import time
from flask import Flask, render_template, request

from subprocess import check_output
import subprocess
import os



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)


number = 0

flash = 10

myCmd = os.popen('/opt/vc/bin/vcgencmd measure_temp').read()

app = Flask(__name__)


@app.route('/')
def main():
   
    return render_template('index.html', the_title='WebServer Flask-Raspberry_PI_4 ' )

def log_request():
    with open('vsearch.log', 'a') as log:
        print(number, myCmd, file=log)
        
        
        

@app.route('/<action>', methods=['GET','POST'])



def control(action):
    
    if action == 'on':
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
        
        
        for i in range(flash):
            global number
            number += 1
            
            GPIO.output(12,True)
            time.sleep(0.5)
            
            
            GPIO.output(12,False)
            time.sleep(0.5)
            
 
    if action == 'stop':
        GPIO.output(12,False)
        print("Была нажата кнопка ВЫКЛЮЧИТЬ")
    
    
    GPIO.cleanup()
        
    
    print(myCmd, number)
    log_request()
   
                    
    return render_template('index.html', the_results = number, the_temperature = myCmd)





#запускаем веб-сервер
if __name__ == '__main__':
    app.run( host='192.168.0.20', port=5400, debug=True)
    




