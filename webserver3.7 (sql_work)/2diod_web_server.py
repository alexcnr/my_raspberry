#!/usr/bin/env python3
import RPi.GPIO as GPIO 
import time, datetime
from flask import Flask, render_template, request, escape

from subprocess import check_output
import subprocess
import os

import sqlite3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)


number = 0 #счетчик миганий светодиода

name = 0 #имена процессов миганий

rez_number = 0




flash = 10 #количество запланированных миганий

myCmd = os.popen('/opt/vc/bin/vcgencmd measure_temp').read()  #температуру процессора


app = Flask(__name__)




@app.route('/<action>', methods=['GET','POST'])


def control(action):
    global name
    global number
    global rez_number
    
    
    
    if action == 'on':
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
                
        name += 1
 
        for i in range(flash):
            
            number += 1
            
            GPIO.output(12,True)
            time.sleep(0.5)
            
            
            GPIO.output(12,False)
            time.sleep(0.5)
 
    if action == 'stop':
        GPIO.output(12,False)
        
        
        rez_number = number
        number = 0
        

        print("Была нажата кнопка ВЫКЛЮЧИТЬ", rez_number)
        print("name - ", name, "rez_number - ", rez_number, "number - ", number)
        today = datetime.datetime.today()
        
        general_log = log_request(request) #отправка данных в файл лог и эти же данные по почте
        message = "Миганий светодиода было: {}. Краткий лог процесса: {}. And CPU {}. Date and time: {}".format(rez_number, general_log, myCmd, today.strftime("%Y-%m-%d-%H.%M.%S")).encode('utf-8') #сообщение в письмо

        GPIO.cleanup()
        
        date_time = datetime.datetime.today()
        date_time = date_time.strftime("%Y-%m-%d; %H.%M.%S")
        
     ####          SQL                 ###
        
        conn = sqlite3.connect('flashdb.sqlite')
        cur = conn.cursor()

        #cur.execute('DROP TABLE IF EXISTS Counts')

        #flash - name of process,  count -  count of flashes, 

        cur.execute('''
                CREATE TABLE IF NOT EXISTS Counts (
            flash TEXT,
            count INTEGER,
            temp_CPU TEXT,
            date_time TEXT) ''')

        cur.execute('''INSERT INTO Counts (flash, count, temp_CPU, date_time)
             VALUES (?, ?, ?, ?)''', (name, rez_number, myCmd, date_time) )


        conn.commit()
        cur.close()

 

    return render_template('index.html', the_results = rez_number, the_temperature = myCmd)


@app.route('/')
def main():
   
    return render_template('index.html', the_title='WebServer Flask-Raspberry_PI_4 ' )

        
def log_request(req: 'flask_request'):
    """Возвращает результаты работы в файл, а на основании result_request
формируется message для email

"""
    with open('global.log', 'a') as log:
        print("Имя процесса - " + str(name), file=log)
        print("Количество миганий - " + str(rez_number), myCmd, file=log)
        print(req.remote_addr,req.method, file=log)#IP адрес браузера приславшего данные
        print(req.user_agent, file=log) #браузер пользователя
        result_request = req.host_url, req.method, req.user_agent #
        return result_request

@app.route('/log')
def view_the_log():
    contents = []
    with open ('global.log') as log:
        for line in log:
            contents.append([]) #делаем кортеж списков
            for item in line.split('. '): #разбить строку по разделителю и обработать каждый полученный элемент в списке
                contents[-1].append(escape(item)) #записать в конец списка, находящегося в конце contents 
                print(item)
    titles = ('Number', 'MyCmd', 'Remote_addr', 'Method', 'User_agent') #заголовки для таблицы


    return render_template('log.html', 
                            the_title = 'View Log',
                            the_row_titles = titles,
                            the_data = contents,  )


if __name__ == '__main__':
    app.run( host='192.168.0.20', port=5301, debug=True)
    
    

    




