from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import copy
from urllib.request import urlopen
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from prettytable import PrettyTable
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
import pickle
import time
import pickle
import os
from selenium.webdriver.chrome.options import Options
import numpy as np
# # Use the `install()` method to set `executabe_path` in a new `Service` instance:
# service = Service(executable_path=ChromeDriverManager().install())
#
# # Pass in the `Service` instance with the `service` keyword:
# driver = webdriver.Chrome(service=service)
linklist=['https://racing.hkjc.com/racing/information/chinese/Horse/Horse.aspx?HorseId=HK_2019_D205','https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx?HorseId=HK_2020_E025&Option=1','https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx?HorseId=HK_2019_D491','https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx?HorseId=HK_2020_E147','https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx?HorseId=HK_2019_D121','https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx?HorseId=HK_2019_D113','https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx?HorseId=HK_2020_E123']


import sys
import traceback

def saveh(object):
    pass

def loadf(name):
    pass



def url_to_file(url, driver=None,debugprint=False,folder='data'):
    pos1 = url.find('_', 1)
    id = url[pos1 + 1:pos1 + 10]

    if driver is None:
        f = BeautifulSoup(urlopen(url).read())

    else:
        driver.get(url)
        time.sleep(4)
        print(f"read {url} from Chrome")
        f = BeautifulSoup(driver.page_source)




    #print(driver.page_source)
    #f = BeautifulSoup(urlopen(url).read())

    if debugprint:
        print(f.prettify())
    tname = id
    print(f"    read {tname}Web")


    mtabel = f.find(text='馬場/跑道/').find_parent().find_parent().find_parent().find_all("tr")

    data = []
    for i in mtabel:
        row = []
        if '馬季'  not in  str(i) and '途程'  not in  str(i):
            for d in i.find_all('td'):
                if d.text.strip()  not in '':
                    row.append(d.text.strip())
            data.append(copy.deepcopy(row))
    if debugprint:
        print(tabulate(data))
    print(len(data),len(data[0]))
    result=np.zeros((len(data),8),dtype=int)
    data = [x for x in data if x != []]

    for i in range(len(data)):

        result[i][0]= 0 if '海外' in str(data[i][0]) or '此季' in str(data[i][0]) else int(data[i][0])
        result[i][1]=str(data[i][2]).replace('/','')
        result[i][2]= int(data[i][4])
        result[i][3]='好' in str(data[i][5])
        result[i][4] = '快' in str(data[i][5])

        result[i][5] = 0 if '--' in str(data[i][13]) else int(data[i][13])
        result[i][6] = 0 if '--' in str(data[i][16]) else int(data[i][16])
        result[i][7] = 0 if '--' in (str(data[i][15]).replace('.','')) else (str(data[i][15]).replace('.',''))
    print(result[0,0])
    np.save(f"{folder}/{id}",result)

def reget(links,node,foder='data'):
    option=Options()
    option.headless=True
    driver = webdriver.Chrome(options=option)
    filelist = os.listdir(foder)
    print("R start---------------------------------------------------------------------------------------------------------")
    fail=[]
    for i in links:
        try:
            #print(i)
            pos1=i.find('_',1)
            id=i[pos1+1:pos1+10]
            if f"{id}.npy" in filelist:
                print(f"{id} in file already --skiping")
                continue
            url_to_file(i,driver=driver,folder=foder)
        except Exception as e  :
            print('fail hourse')
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
            fail.append(i)
    if(fail!=[]) and node>0:

        reget(fail,node-1)
#reget([linklist[0]],1)
# # print(len(linklist))
#url_to_file('https://racing.hkjc.com/racing/information/chinese/Horse/Horse.aspx?HorseId=HK_2019_D095&Option=3',debugprint=True,folder='data2')

