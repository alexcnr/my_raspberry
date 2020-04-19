
import RPi.GPIO as GPIO 
import time
from flask import Flask, render_template, request

GPIO.setwarnings(False)


app = Flask(__name__)


@app.route('/')
def main():
   
    return render_template('index.html' )


@app.route('/<action>')


def control(action):
    
    if action == 'on':
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
        for i in range(10):
            GPIO.output(12,True)
            time.sleep(0.5)
            GPIO.output(12,False)
            time.sleep(0.5)

    if action == 'stop':
        GPIO.output(12,False)
        print("Была нажата кнопка ВЫКЛЮЧИТЬ")
    
    
    GPIO.cleanup()
        
        
                    
    return render_template('index.html')
     

    



#запускаем веб-сервер
if __name__ == '__main__':
    app.run( host='192.168.0.20', port=5000, debug=True)
    




