
import RPi.GPIO as GPIO 
import time, datetime
from flask import Flask, render_template, request

from subprocess import check_output
import subprocess
import os
import smtplib, ssl
from mail_def import mail_sender



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

#req_rez = None
number = 0 #счетчик миганий светодиода

flash = 10 #количество запланированных миганий

myCmd = os.popen('/opt/vc/bin/vcgencmd measure_temp').read()  #температуру процессора

message = None #переменная для сообщения по эл.почте


app = Flask(__name__)


@app.route('/')
def main():
   
    return render_template('index.html', the_title='WebServer Flask-Raspberry_PI_4 ' )

def log_request(req: 'flask_request'):
    """Возвращает результаты работы в файл, а на основании result_request
формируется message для email

"""
    with open('global.log', 'a') as log:
        print("Количество миганий - " + str(number), myCmd, file=log)
        print(req.remote_addr,req.method, file=log)#IP адрес браузера приславшего данные
        print(req.user_agent, req.url, file=log) #браузер пользователя
        result_request = req.host_url, req.method, req.user_agent #
        return result_request
        

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
        print("Была нажата кнопка ВЫКЛЮЧИТЬ", number)
        today = datetime.datetime.today()
        
        general_log = log_request(request) #отправка данных в файл лог и эти же данные по почте
        message = "Миганий светодиода было: {}. Краткий лог процесса: {}. And CPU {}. Date and time: {}".format(number, general_log, myCmd, today.strftime("%Y-%m-%d-%H.%M.%S")).encode('utf-8') #сообщение в письмо

        #message = "Flash " + str(number) + str(general_log) + "  and CPU " + myCmd + today.strftime("%Y-%m-%d-%H.%M.%S") #сообщение в письмо
        mail_sender(message) #вызов функции из модуля mail_def.py
        
       
        GPIO.cleanup()

    return render_template('index.html', the_results = number, the_temperature = myCmd)

    number = 0
#запускаем веб-сервер
if __name__ == '__main__':
    app.run( host='192.168.0.20', port=5400, debug=True)
    
    

    




