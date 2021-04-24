import time
from datetime import datetime, timedelta, timezone
import pymysql
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

stopbtn = 'n'
sT = 0
url = "http://jinoiot.com/"

stateTimeOne = datetime.strptime('2020-07-01 12:40:00', '%Y-%m-%d %H:%M:%S')
stateTimeTwo = datetime.strptime('2020-07-01 12:40:05', '%Y-%m-%d %H:%M:%S')

stateTime = stateTimeTwo - stateTimeOne


options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!

browser = webdriver.Chrome('chromedriver')##, options=options) # 인터페이스에 보이지 않게 접속하기 위함
browser.set_window_size(2048, 1500)
## 브라우저 시작
browser.get(url)
###############################로그인 시작############################
time.sleep(1.5)
login = {
    "id" : "admin",
    "pw" : "alluhak123~",
    "input" : "박선용",
    "input2" : "S100-063BJ-CAJC"
}

# 아이디와 비밀번호를 입력합니다.
time.sleep(0.5) ## 0.5초
browser.find_element_by_xpath('//*[@id="header"]/div[2]/ul/li[4]/a').click()
# driver.find_element_by_name('id').send_keys('아이디') # "아이디라는 값을 보내준다"
time.sleep(1) ## 0.5초
browser.find_element_by_name('mid').send_keys(login.get("id"))
time.sleep(0.5) ## 0.5초
browser.find_element_by_name('mpwd').send_keys(login.get("pw")) 
browser.find_element_by_xpath('//*[@id="content"]/div[4]/form/ul/li[3]/a').click()
#####################################################################
time.sleep(1)
browser.find_element_by_xpath('//*[@id="slt"]/option[3]').click()
time.sleep(0.5)
browser.find_element_by_xpath('//*[@id="sch"]').send_keys(login.get("input")) 
time.sleep(0.5)


browser.find_element_by_xpath('//*[@id="content"]/section/table/tbody/tr/td[3]/a').click()
time.sleep(0.5)
browser.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[2]/td[3]').click()
time.sleep(0.5)
browser.find_element_by_xpath('//*[@id="content"]/ul[1]/li[2]').click()
time.sleep(0.5)


#MySQL Connection 연결
conn = pymysql.connect(host='safec.cafe24.com', user='safec', password='ftppiluhak123',
    db='safec', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = conn.cursor()
print()
def runT():
    global stateTime
    while 1:
        
        #IoT plannet에서 LoRa 통신 모듈의 데이터 값을 가진 javascrip의 HTML 경로
        data = browser.find_element_by_xpath('//*[@id="tab2"]/section/table/tbody').find_elements_by_tag_name('tr')[1]
        data = data.text

        print()
        print("jinoIoT LoRa 모듈 데이터 값입니다.\n")

        name = 'G1'
        data = data.split(' ')
        date = data[0] + " " + data[1]
        sensing = data[2]

        TimeOne = datetime.now()
        TimeOne = str(TimeOne)[:-7]
        TimeOne = datetime.strptime(TimeOne, '%Y-%m-%d %H:%M:%S')
        TimeTwo = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        
        print(date+ " " +sensing)
        
        print(TimeOne)
        print(TimeTwo)
        
        compareT = TimeOne - TimeTwo
        
        print(compareT)
        
        if compareT <= stateTime:

            # SQL문 실행
            sql1 = """INSERT INTO wallj(name, sensing, date) VALUES (%s, %s, %s)"""
            curs.execute(sql1, (name, sensing, date))
            print("OK")
        
        
        browser.execute_script("location.reload()")
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="content"]/ul[1]/li[2]').click()
    
       
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
            break
t1 = Thread(target = runT, args=())
t1.start()

print("Are you want to stop? (Yes: enter the y, No: wait or anther)")

while 1:
    stopbtn = input()
    if stopbtn == 'y':
        break





