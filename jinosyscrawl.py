import time
from datetime import datetime, timedelta, timezone
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

url = "http://krict-cms.krict.re.kr/c_product_list.do"

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!

browser = webdriver.Chrome('chromedriver')#, options=options) # 인터페이스에 보이지 않게 접속하기 위함
browser.set_window_position(0, 0)
browser.set_window_size(800, 1000)
browser.get(url)

time.sleep(3)

list_str = ""
no, name, com, CAT, CAS, grade = [],[],[],[],[],[]

j = 0
i = 2
z = 0
while True :
    table = browser.find_element_by_class_name('chart')
    tbody = table.find_element_by_tag_name("tbody")
    while True :
        try :
            rows = tbody.find_elements_by_tag_name("tr")[j]
            td = rows.find_elements_by_tag_name("td")
            
            for index, value in enumerate(td):
                list_str += value.text + "@"
            n, na, c, C, CA, g, nu = list_str.split("@")
            no.append(n)
            name.append(na)
            com.append(c)
            CAT.append(C)
            CAS.append(CA)
            grade.append(g)
            j += 1
            print(no[len(no)-1], name[len(name)-1], com[len(com)-1], CAT[len(CAT)-1], CAS[len(CAS)-1], grade[len(grade)-1])
            print("\n success \n")
            list_str = ""
            z += 1
        except :
            j = 0
            list_str = ""
            print("next")
            break
        

    i += 1
    try :
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div/div[3]/a['+str(i)+']').click()
        time.sleep(1)
        print("scroll success")
    except :
        for p in range(z):
            print("scroll fail")
            no.pop()
            name.pop()
            com.pop()
            CAT.pop()
            CAS.pop()
            grade.pop()
        i -= 1
    if i == 12:
        i = 2        

browser.close()
browser.quit()