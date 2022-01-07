from hoursedata import *
import os
import numpy as np
#import tensorflow as tf
import datetime
# main
import random
# read data and organize data in directory to generate final.npy file
racefoder='race2'
datafoder= 'data3'
No_of_hourse=12
required_data_no=3
def strdate_to_date(inpuydate):
    inpuydate = str(inpuydate)
    length = len(str(inpuydate))
    x = datetime.datetime.now()
    if length == 5:
        # print(int(str('20'+inpuydate[-2::])),int(inpuydate[-4:-2]),int(inpuydate[-5]))
        x = datetime.datetime(int(str('20' + inpuydate[-2::])), int(inpuydate[-4:-2]), int(inpuydate[-5]))
    if length == 6:
        # print(int(str('20'+inpuydate[-2::])),int(inpuydate[-4:-2]),int(inpuydate[0:2]))
        x = datetime.datetime(int(str('20' + inpuydate[-2::])), int(inpuydate[-4:-2]), int(inpuydate[0:2]))
    if length == 7:
        # print(int(str(inpuydate[-4::])),int(inpuydate[-6:-4]),int(inpuydate[-7]))
        x = datetime.datetime(int(str(inpuydate[-4::])), int(inpuydate[-6:-4]), int(inpuydate[-7]))
    if length == 8:
        # print(int(str(inpuydate[-4::])),int(inpuydate[-6:-4]),int(inpuydate[0:2]))
        x = datetime.datetime(int(str(inpuydate[-4::])), int(inpuydate[-6:-4]), int(inpuydate[0:2]))

    return x.date()


def fsecond_to_ltime(itime):
    itime = str(itime)
    output = int(itime[-4:])
    if len(itime) == 5:
        output += int(itime[0]) * 6000
    return output



file_list_race=[x if int(No_of_hourse)== int(x[0:2]) else '' for x in os.listdir(racefoder)]
file_list_race=list(filter(None,file_list_race))
print(list(file_list_race))
print(len(list(file_list_race)))
validdata=0
listoffinaldataINPUT=[]
listoffinaldataOUPUT=[]

for i in range(len(file_list_race)):
    try:
        race_array=np.load(f'{racefoder}/{file_list_race[i]}')
        assert No_of_hourse==len(race_array)-1 ,'check race array complete or not'
        hourse_unsorteddata=[] # list of np array

        # find venue
        venue=file_list_race[i][-10:-8]
        print(venue,' ')

        for j in range(No_of_hourse):
            try:
                temp=np.load(f"{datafoder}/{race_array[j]}.npy") # open hourse data
                tempresult=[]

                for k in range(len(temp)):

                    if not(np.array_equal(temp[k],np.zeros(8,dtype=int)) or  0 == temp[k][0]
                           or  0 == temp[k][1]or  0 == temp[k][2]or  0 == temp[k][5]
                           or  0 == temp[k][6]or 0 == temp[k][7]):
                        tempresult.append(np.asarray(temp[k]))

                hourse_unsorteddata.append(np.asarray(tempresult))
            except Exception as e:
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

        assert len(hourse_unsorteddata)==No_of_hourse ,'loss hourse data !!! '
        hourse_unsorteddata=np.asarray(hourse_unsorteddata)

        # print(hourse_unsorteddata)
        # print(type(hourse_unsorteddata))
        # print(type(hourse_unsorteddata[0]))
        # print(type(hourse_unsorteddata[0][0]))
        # print(type(hourse_unsorteddata[0][0][0]))

        # print(type(race_array))

        ####
        tresult = str(file_list_race[i][3:11])
        race_id = str(file_list_race[i][-7:-4])




        tresult=strdate_to_date(tresult)
        print(race_id,end=' ')
        print(tresult,end=' ')

        print('-----')

        valid=True
        listoffinaldata=[]
        for j in range(len(hourse_unsorteddata)):
            assert valid ,f"Not valid hourse {str(j)}   "
            found =False
            counter=0
            hourseKfinaldata=[]
            for k in range(len(hourse_unsorteddata[j])):
                if (int(race_id)==hourse_unsorteddata[j][k][0]) and (tresult==strdate_to_date(hourse_unsorteddata[j][k][1])):

                    found=True
                    hourse_unsorteddata[j][k][7] = fsecond_to_ltime(hourse_unsorteddata[j][k][7])
                    hourse_unsorteddata[j][k][1] = (strdate_to_date(hourse_unsorteddata[j][k][1]) - tresult).days
                    print("founded" + str(hourse_unsorteddata[j][k][7]),end='  ')
                    #print(j[k])
                    continue
                if found and tresult>strdate_to_date(hourse_unsorteddata[j][k][1])and counter<required_data_no:
                    hourse_unsorteddata[j][k][7]=fsecond_to_ltime(hourse_unsorteddata[j][k][7])
                    hourse_unsorteddata[j][k][1]=(strdate_to_date(hourse_unsorteddata[j][k][1])-tresult).days
                    hourseKfinaldata.append(hourse_unsorteddata[j][k])
                    #print(j[k])


                    counter+=1
            assert found ,'Not found '
            assert counter==required_data_no , 'not enough data'
            hourseKfinaldata=np.asarray(hourseKfinaldata)
            listoffinaldata.append(np.array([j,hourseKfinaldata]))
            #print(hourseKfinaldata)
            #print(counter)

        random.shuffle(listoffinaldata)
        listoffinaldata=np.asarray(listoffinaldata)
        #print(listoffinaldata)
        #print(listoffinaldata.shape)
        suboutputt=[x[0] for x in listoffinaldata]
        suboutput=[]
        for x in range(len(suboutputt)):
            if suboutputt[x]==1 :
                suboutput.append(int(x))

        subinput=[x[1] for x in listoffinaldata]
        print()
        print(suboutput)
        validdata+=1
        subinput.append(np.full((required_data_no,8),race_array[len(race_array)-1]))
        subinput.append(np.asarray(suboutput))
        print(subinput)
        listoffinaldataINPUT.append(np.asarray(subinput))
        listoffinaldataOUPUT.append(np.asarray(suboutput))
    except Exception as e:
        print(e)




print(validdata)
listoffinaldataINPUT=np.asarray(listoffinaldataINPUT)
listoffinaldataOUPUT=np.asarray(listoffinaldataOUPUT)
print(listoffinaldataINPUT.shape)
print(listoffinaldataOUPUT.shape)



np.save(f"{No_of_hourse}_{required_data_no}_F",listoffinaldataINPUT)







