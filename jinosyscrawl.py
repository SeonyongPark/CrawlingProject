import time
import pymysql
import sys
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

browser = webdriver.Chrome('chromedriver', options=options) # 인터페이스에 보이지 않게 접속하기 위함
browser.set_window_position(0, 0)
browser.set_window_size(800, 1000)
browser.get(url)

tlist1 = []
tlist2 = []
tlist3 = []
total_list = []


# MySQL Connection 연결
conn = pymysql.connect(host='safec.cafe24.com', user='safec', password='ftppiluhak123',
    db='safec', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = conn.cursor()

def bring_table(i):
    global tlist1, tlist2, tlist3
    num = 1
    name = "chart2"
    path = '/html/body/div/div/form/div/table[1]'
    list_str = ""
    while True :
        j = 0
        try:
            if i == 3:
                table1 = browser.find_element_by_xpath(path)
                tbody1 = table1.find_element_by_tag_name("tbody")
                
            else :
                table1 = browser.find_element_by_class_name(name)
                tbody1 = table1.find_element_by_tag_name("tbody")

            while True :
                try :
                    rows1 = tbody1.find_elements_by_tag_name("tr")[j]
                    td1 = rows1.find_elements_by_tag_name("td")
                    
                    for _, value in enumerate(td1):
                        if value.text == "":
                            list_str += "null@"
                        else :
                            list_str += value.text + "@"
                    j += 1
                except :
                    name = name[:-1]
                    path = path.replace(str(num), str(num+1))
                    break
            num += 1
        except:
            break
    
    #= list_str.split("@")
    #sql1 = """INSERT INTO IoT(name, x, y, temp, mois, state) VALUES (%s, %s, %s, %s, %s, %s)"""
    #curs.execute(sql1, (namedata, x, y, ondodata, isthedata, copydata))
    if i == 1:
        print(list_str.count("@"))
        tlist = list_str.split("@")  
        info, cas, ke, un, eu, name, tinnitus, gravity, cat, manu, distributor, standard, exp1, exp2, inpu = tlist[0:15] 
        #print("제품번호 = {0}\n".format(info), "CAS = {0}\n".format(cas), "KE No. = {0}\n".format(ke), "UN No. = {0}\n".format(un), "EU No. = {0}\n".format(eu), 
        #"제품명 = {0}\n".format(name), "이명 = {0}\n".format(tinnitus), "비중 = {0}\n".format(gravity), "CAT = {0}\n".format(cat), 
        #"제조사 = {0}\n".format(manu), "유통사 = {0}\n".format(distributor), "표준 = {0}\n".format(standard),  "exp1 = {0}\n".format(exp1)
        #,  "exp2 = {0}\n".format(exp2), "inpu = {0}\n".format(inpu), "measure = {0}\n".format(measure), spec, unit)
        sql1 = """INSERT INTO ChemicalReagenInfomation(Info, CAS, KE, UN, EU, Name, Tinnitus, Gravity, CAT, Manu, Distributor, Standard, ExpirationDateOpen, ExpirationDateNotOpen, Input)
         VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s)"""
        curs.execute(sql1, (info, cas, ke, un, eu, name, tinnitus, gravity, cat, manu, distributor, standard, exp1, exp2, inpu))
        sql2 = """INSERT INTO ChemicalReagentProductSpec(CAT, Measure, Spec, Unit)
        VALUES (%s,%s,%s,%s)
        """
        for o in range(15, len(tlist)-3, 3):
            curs.execute(sql2, (cat, tlist[o], tlist[o+1], tlist[o+2]))

    elif i == 2:
        tlist1 = list_str.split("@")
    elif i == 3:
        tlist2 = list_str.split("@")
    elif i == 4:
        tlist3 = list_str.split("@")
        total_list = tlist1 + tlist2 + tlist3
        while len(total_list) <= 17:
            total_list.append(" ")
            
        sql1 = """INSERT INTO ChemicalReagenComponent(CAS, Cname, Value, MAX, AVG, component, Regulation, Classification, HPhrase, Phrase, Type, RDate, Language, HazardousGradeP, HazardousGradeH) 
        VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s)"""
        curs.execute(sql1, (total_list[2],total_list[3],total_list[4], total_list[5], total_list[6], total_list[0], total_list[7], total_list[9],
         total_list[10], total_list[11], total_list[13], total_list[14], total_list[15], total_list[16], total_list[17]))
    
        
def bring_newlink():
    browser.switch_to_window(browser.window_handles[1])
    browser.get_window_position(browser.window_handles[1])
    i = 1
    while True :
        bring_table(i)
        i += 1
        if i == 5:
            break
        time.sleep(0.5)
        if i < 3:
            xpath = '/html/body/div/div/form/ul/li['+str(i)+']/a'
        else :
            xpath = '/html/body/div/div/form/div/ul/li['+str(i)+']/a'
        
        time.sleep(0.1)
        browser.find_element_by_xpath(xpath).click()
    
    time.sleep(0.5)
    browser.close()
    browser.switch_to_window(browser.window_handles[0])
    browser.get_window_position(browser.window_handles[0])


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

            sql1 = """INSERT INTO ChemicalReagentList(NO, Name, Manu, CAT, CAS, Grade) VALUES (%s, %s, %s, %s, %s, %s)"""
            curs.execute(sql1, (no[len(no)-1], name[len(name)-1],  com[len(com)-1], CAT[len(CAT)-1], CAS[len(CAS)-1], grade[len(grade)-1]))
            rows.find_elements_by_tag_name("td")[1].click()
            print("click")
            time.sleep(1.5)
            bring_newlink()
            browser.switch_to_window(browser.window_handles[0])
            browser.get_window_position(browser.window_handles[0])
            print("\n success \n")
            list_str = ""
        except :
            j = 0
            list_str = ""
            print("next")
            break
        

    i += 1
    try :
        browser.switch_to_window(browser.window_handles[1])
        browser.get_window_position(browser.window_handles[1])
        browser.close()
        browser.switch_to_window(browser.window_handles[0])
        browser.get_window_position(browser.window_handles[0])
        
    except:
        browser.switch_to_window(browser.window_handles[0])
        browser.get_window_position(browser.window_handles[0])


    browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div/div[3]/a['+str(i)+']').click()
    time.sleep(1)
    if i == 12:
        i = 2
    print("scroll success")


browser.close()
browser.quit()