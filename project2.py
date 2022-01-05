#11B10101 서울 = 1
#11F20501 광주 = 3
#11H10701 대구 = 2
#11G00201 제주 = 4


#실시간 영상 포트 : http://ip:8081

import RPi.GPIO as GPIO
import time
from flask import Flask, render_template
import picamera
from urllib.parse import urlencode, unquote
import requests
import json
from bs4 import BeautifulSoup
import socket
import os   #파이썬에서 리눅스 명령어 실행하기 위함
import spidev


#조이스틱
delay = 0.5
sw_channel = 0
vrx_channel = 1
vry_channel = 2

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100000

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data



button_pin = 15
servo_pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(servo_pin,GPIO.OUT)
p = GPIO.PWM(servo_pin, 50)


#Camera = picamera.PiCamera()

def button_callback(channel):   #버튼을 누르게 되면 os를 통해 파이썬에서 리눅스 명령어 실행
    print("on")
    os.system("sudo service motion start") #카메라 켜짐과 동시에 모션감지 기능 on
    os.system("sudo motion -n")

        
def servoMotor(degree):
    p.start(0)
    p.ChangeDutyCycle(degree)
    time.sleep(0.5)

    p.stop()
    GPIO.cleanup(servo_pin)

     
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback)
time.sleep(0.1)




me = socket.socket()    #소켓 생성
me.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    #1초에 1번씩 소켓을 재사용
#me.bind(('172.30.1.21',12345))  #bind() 함수로 ip와 port 번호를 설정
#me.bind(('169.254.203.133',1234))
#me.bind(('172.30.1.5',12345))
me.bind(('172.30.1.5',1234))
me.listen(1)


        
conn, addr = me.accept()    #클라이언트와의 연결을 기다린다
data = conn.recv(1024).decode()
re = conn.recv(1024)
print(re.decode("utf-8"))


            
#conn.send(str(re).encode("utf-8"))
            
   
loc = re.decode("utf-8")
if loc == '1':
    url = 'http://apis.data.go.kr/1360000/VilageFcstMsgService/getLandFcst?serviceKey=RFKv4CbXS/Qn6OUogm1mvTqvk7w85vYYV0AO946MZ35YUyCWPVzEPxV6p1zm7Zjh7y6Pc6RJdYnApvb5ITObHQ==&numOfRows=10&pageNo=1&regId=11B10101'
    loc2 = "서울"
elif loc == '2':
    url = 'http://apis.data.go.kr/1360000/VilageFcstMsgService/getLandFcst?serviceKey=RFKv4CbXS/Qn6OUogm1mvTqvk7w85vYYV0AO946MZ35YUyCWPVzEPxV6p1zm7Zjh7y6Pc6RJdYnApvb5ITObHQ==&numOfRows=10&pageNo=1&regId=11H10701'
    loc2 = "대구"
elif loc == '3':
    url = 'http://apis.data.go.kr/1360000/VilageFcstMsgService/getLandFcst?serviceKey=RFKv4CbXS/Qn6OUogm1mvTqvk7w85vYYV0AO946MZ35YUyCWPVzEPxV6p1zm7Zjh7y6Pc6RJdYnApvb5ITObHQ==&numOfRows=10&pageNo=1&regId=11F20501'
    loc2 = "광주"
else:
    url = 'http://apis.data.go.kr/1360000/VilageFcstMsgService/getLandFcst?serviceKey=RFKv4CbXS/Qn6OUogm1mvTqvk7w85vYYV0AO946MZ35YUyCWPVzEPxV6p1zm7Zjh7y6Pc6RJdYnApvb5ITObHQ==&numOfRows=10&pageNo=1&regId=11G00201'
    loc2 = "제주"

result = requests.get(url)
soup = BeautifulSoup(result.text, "lxml")


items = soup.find_all("item")   #item항목들을 items에 다 넣음

def WF_CD(a):
    if a == 'DB01':
        a = "맑음"
    elif a == 'DB03':
        a = "구름많음"
    else:
        a = "흐림"
    return a


for item in items:
    numEf = item.find('numef').get_text()  #오늘오후=0, 내일오전=1
    regid = item.find('regid').get_text()  #11B10101=seoul
    ta = item.find('ta').get_text()        #예상기온(℃)
    rnSt = item.find('rnst').get_text()    #강수확률
    wfCd = item.find('wfcd').get_text()    #날씨--맑음?

    if(numEf == "0"):
        print("지역 : %s" %(loc2))
        print("예상 기온(°C) : %s°C" %(ta))
        print("강수확률 : " + rnSt + "%")
        print("날씨 : %s" %(WF_CD(wfCd)))
                    


    
#웹서버 구축 http://ip:5000

app = Flask(__name__)
ta = item.find('ta').get_text()

@app.route("/")
def picture():
    return render_template('picture.html')

@app.route('/check')
def check():
    return render_template('travel.html')

if int(ta) >= 5:
    @app.route('/clothes')
    def clothes():
        return render_template('clothes.html')
else:
    @app.route('clothes')
    def clothes():
        return render_template('clothes2.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0")



#조이스틱
while True:
    vrx_pos = readadc(vrx_channel)
    vry_pos = readadc(vry_channel)

    sw_val = readadc(sw_channel)

    if vrx_pos >=800:
        servoMotor(2.5)
        time.sleep(delay)
    elif vry_pos >=800:
        servoMotor(12.5)
        time.sleep(delay)
    elif sw_val == 0:
        break









