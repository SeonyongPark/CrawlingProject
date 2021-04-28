import time
import pymysql
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import sys
from datetime import datetime, timedelta, timezone

x = ''
y = ''
namedata = ''
ondodata = ''
xirodata = ''
isthedata = ''
copydata = ''

stopbtn = 'n'




url = "http://www.iotplanet.co.kr/loginUI"
iot_url = "http://www.iotplanet.co.kr/dashboard/dashboardUI"

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR")  #한국어!
browser = webdriver.Chrome('chromedriver')#, options=options) # 인터페이스에 보이지 않게 접속하기 위함
browser.get(url)
Statebrowser = webdriver.Chrome('chromedriver')#, options=options) # 인터페이스에 보이지 않게 접속하기 위함
Statebrowser.get(url)


###############################로그인 시작############################
time.sleep(1.5)
login = {
    "id" : "jinosys2",
    "pw" : "a1234567890!"
}

# 아이디와 비밀번호를 입력합니다.
time.sleep(0.5) ## 0.5초
# driver.find_element_by_name('id').send_keys('아이디') # "아이디라는 값을 보내준다"
browser.find_element_by_name('loginID').send_keys(login.get("id"))
time.sleep(0.5) ## 0.5초
browser.find_element_by_name('passwd').send_keys(login.get("pw")) 
browser.find_element_by_xpath('//*[@id="loginBtn"]').click()
time.sleep(0.5)

## 통신상태 값을 가져오기 위해 브라우저를 하나 더 실행시킨다.
Statebrowser.find_element_by_name('loginID').send_keys(login.get("id"))
time.sleep(0.5) ## 0.5초
Statebrowser.find_element_by_name('passwd').send_keys(login.get("pw")) 
Statebrowser.find_element_by_xpath('//*[@id="loginBtn"]').click()
time.sleep(0.5)
Statebrowser.find_element_by_xpath('//*[@id="topDivBox_1"]/div/div[2]').click()
time.sleep(0.5)
Statebrowser.find_element_by_xpath('//*[@id="table"]/tbody/tr[1]/td[16]/button').click()
#####################################################################
time.sleep(2)

# MySQL Connection 연결
conn = pymysql.connect(host='safec.cafe24.com', user='safec', password='ftppiluhak123',
    db='safec', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = conn.cursor()

def runT():

    global ondodata, xirodata, isthedata, namedata, copydata

    while 1:

        if stopbtn == 'y':
            break

        #IoT plannet에서 LoRa 통신 모듈의 데이터 값을 가진 javascrip의 HTML 경로
        ondo = browser.find_element_by_xpath('//*[@id="widget_1660"]/div/div[2]/div').find_element_by_tag_name('label')
        xiro = browser.find_element_by_xpath('//*[@id="widget_1658"]/div/div[2]/div').find_element_by_tag_name('label')
        isthe = browser.find_element_by_xpath('//*[@id="widget_1661"]/div/div[2]/div').find_element_by_tag_name('label')
        name = browser.find_element_by_xpath('//*[@id="widget_1658"]/div/div[1]').find_element_by_tag_name('div')
        copy = Statebrowser.find_element_by_xpath('//*[@id="detailView"]/table[1]/tbody/tr[1]/td[2]').find_element_by_tag_name('span')
        
        copydata = copy.text
        ondodata = ondo.text
        xirodata = xiro.text
        isthedata = isthe.text
        namedata = name.text


        ## state데이터의 잡 기호들을 제거 해주는 부분
        copydata = copydata.replace("●", "")
        copydata = copydata.replace("(", "")
        copydata = copydata.replace(")", "")
        copydata = copydata.replace(" ", "")
        

        def Mysplit():
            i = 0
            global xirodata, x, y

            for i in range(len(xirodata)):
                if xirodata[i] == '3':
                    if xirodata[i + 1] == '6':
                        if i == 0:
                            x = '0'
                            y = xirodata[i+3: len(xirodata)+1]
                            break
                        elif xirodata[i+2] == '0':
                            x = xirodata[0:i]
                            y = xirodata[i+3:len(xirodata)]
                            break

        Mysplit()

        print("IoTplannet LoRa 모듈 데이터 값입니다.\n")
        print(namedata)
        print(x)
        print(y)
        print(ondodata)
        print(isthedata)
        print(copydata)
    
        # SQL문 실행
        sql1 = """INSERT INTO IoT(name, x, y, temp, mois, state) VALUES (%s, %s, %s, %s, %s, %s)"""
        sql = "select * from IoT"
        curs.execute(sql1, (namedata, x, y, ondodata, isthedata, copydata))
        curs.execute(sql)

        #rows = curs.fetchall()
        #print(rows)     # 전체 rows
        
  
        fT = datetime.now()
        while 1:
            sT = datetime.now()
            if stopbtn == 'y':
                break
            
            tt = (sT - fT).seconds
            
            if tt >= 1:
                break
        if stopbtn == 'y':
            conn.close()
            browser.close()
            browser.quit()
            Statebrowser.close()
            Statebrowser.quit()
            break
t1 = Thread(target = runT, args=())
t1.start()

print("Are you want to stop? (Yes: enter the y, No: wait or anther)")

while 1:
    stopbtn = input()
    if stopbtn == 'y':
        break

