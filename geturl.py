from    hoursedata import *
import time
import re
from datetime import datetime, timedelta
from selenium import webdriver
import os
import numpy as np

driver = webdriver.Chrome()
x=datetime(2014,12,29)#YMD
x.strftime("%Y/%m/%d")
dt=timedelta(days=1)
def getrace(url,foder='data',all=False):
    driver.get(url)
    print(url)
    time.sleep(4)
    f = BeautifulSoup(driver.page_source)
    # print(f.prettify())
    a = f.find_all(href=True)

    data = []

    for i in a:
        s = i['href']

        if 'HorseId' in str(s):
            print(s)
            data.append('https://racing.hkjc.com' + s)
    data=dict.fromkeys(data)
    print(data)

    distance=str(f.find(text=re.compile("0米")))
    pos=distance.find('米')
    distance=distance[0:pos]
    distance=int(re.search(r'\d+', distance).group())
    print(distance)

    raceid = str(f.find(text=re.compile(" 場 \(")))
    print(raceid)
    pos = raceid.find('(')+1
    raceid = raceid[pos:pos+3].replace(')','')
    raceid=str("{:03}".format(int(raceid)))

    print(raceid)
    if all:
        data=list(dict(data).keys())
        for i in range(len(data)):
            pos1 = data[i].find('_', 1)
            id = data[i][pos1 + 1:pos1 + 10]
            data[i]= f'https://racing.hkjc.com/racing/information/chinese/Horse/Horse.aspx?HorseId=HK_{id}&Option=1'


    reget(data, 2,foder=foder)
    iddata=[]
    for i in data:
        pos1 = i.find('_', 1)
        id = i[pos1 + 1:pos1 + 10]
        iddata.append(id)

    result=np.asarray(iddata)
    result=np.append(result,[distance])
    print(result)
    no_ofh="{:02}".format(len(data))
    pos=url.find("=")
    Year=url[pos+1:pos+5]
    Month=str("{:02}".format(int(url[pos+6:pos+8])))
    Day=str("{:02}".format(int(url[pos+9:pos+11])))
    pos=url.find("Racecourse=")
    venue=url[pos+11:pos+13]
    print(f"{no_ofh}_{Day}{Month}{Year}_{venue}_{raceid}")
    np.save(f"race2/{no_ofh}_{Day}{Month}{Year}_{venue}_{raceid}",result)
    return len(data)

venue='ST'
print(venue)
for i in range(365*4):

    for j in range(8):
        url=f'https://racing.hkjc.com/racing/information/chinese/Racing/LocalResults.aspx?RaceDate={x.strftime("%Y/%m/%d")}&Racecourse={venue}&RaceNo={int(j+1)}'

        try:
            if getrace(url,foder='data3',all=True)==0:
                break
        except Exception as e:
            print("fail in day")
            print(e)
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
            break




    x-=dt

driver.close()

# closing browser

