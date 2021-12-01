import os
import sys
import re
import datetime
import time
import math
import json
import requests
import urllib.parse
import urllib.request
import sqlite3

from bs4 import BeautifulSoup
from flask import Flask

headers = { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36" }

client_id = 'ThEA6y6LOyfCIqhBFfZC'
client_secret = 'YSiKwyQoqG'

# 도시 가져오기
def get_land_region_root():
    global no, cur
    url = "https://new.land.naver.com/api/regions/list?cortarNo=0000000000"

    try:
        result_code = requests.get(url, headers=headers)
        if result_code.status_code == 200:
            response_body = result_code.text
            response_body_dict = json.loads(response_body)
            
            for item_index in range(0, len(response_body_dict['regionList'])):
                centerLat = response_body_dict['regionList'][item_index]['centerLat']
                centerLon = response_body_dict['regionList'][item_index]['centerLon']
                cortarName = response_body_dict['regionList'][item_index]['cortarName']
                cortarNo = response_body_dict['regionList'][item_index]['cortarNo']
                cortarType = response_body_dict['regionList'][item_index]['cortarType']
                
                print(cortarNo)

                no += 1
                
                cur.executemany('INSERT INTO naver_land_region VALUES (?, ?, ?, ?, ?, ?) ',
                                [(no, cortarNo, cortarName, centerLat, centerLon, cortarType)]
                                )
                                
                get_land_region_sub(cortarNo)

    except Exception as e:
        print('예외가 발생했습니다.', e)
        return "false"
    
    return "true"

# 세부지역 가져오기
def get_land_region_sub(subNo):
    global no, cur
    url = "https://new.land.naver.com/api/regions/list?cortarNo="+subNo

    result_code = requests.get(url, headers=headers)
    if result_code.status_code == 200:
        response_body = result_code.text
        if response_body.find('regionList') > 0 :
            response_body_dict = json.loads(response_body)
            
            for item_index in range(0, len(response_body_dict['regionList'])):
                centerLat = response_body_dict['regionList'][item_index]['centerLat']
                centerLon = response_body_dict['regionList'][item_index]['centerLon']
                cortarName = response_body_dict['regionList'][item_index]['cortarName']
                cortarNo = response_body_dict['regionList'][item_index]['cortarNo']
                cortarType = response_body_dict['regionList'][item_index]['cortarType']
                
                no += 1
                print(cortarNo)
                
                cur.executemany('INSERT INTO naver_land_region VALUES (?, ?, ?, ?, ?, ?) ',
                                [(no, cortarNo, cortarName, centerLat, centerLon, cortarType)]
                                )
                                
                get_land_region_sub(cortarNo)

# 지역별 영역 가져오기
def select_land_region():
    global no, cur
    url = "https://new.land.naver.com/api/cortars?zoom=16&cortarNo="

    try:
        cur.execute("SELECT * FROM naver_land_region WHERE cortarNo = '1141011500' AND cortarType = 'sec'  AND (leftLon is null or leftLon = '')")

        rows = cur.fetchall()

        for row in rows:
            cortarNo = row[1]
            centerLat = float(row[3])
            centerLon = float(row[4])
            topLat = centerLat
            bottomLat = centerLat
            leftLon = centerLon
            rightLon = centerLon

            # 영역가져오기
            result_code = requests.get(url+cortarNo, headers=headers)

            if result_code.status_code == 200:
                response_body = result_code.text
                print(">>>>>>>>> cortarNo : " + response_body[:30])
                
                if response_body.find('cortarVertexLists') > 0 :
                    response_body_dict = json.loads(response_body)
                    for item_index in range(0, len(response_body_dict['cortarVertexLists'][0])):
                        centerLat = float(response_body_dict['cortarVertexLists'][0][item_index][0])
                        centerLon = float(response_body_dict['cortarVertexLists'][0][item_index][1])
                        if topLat < centerLat:
                            topLat = centerLat
                        if bottomLat > centerLat:
                            bottomLat = centerLat
                        if leftLon > centerLon:
                            leftLon = centerLon
                        if rightLon < centerLon:
                            rightLon = centerLon
                no += 1
                cur.execute("UPDATE naver_land_region SET topLat = ?, bottomLat = ?, leftLon = ?, rightLon = ? WHERE cortarNo = ?",(topLat, bottomLat, leftLon, rightLon, cortarNo))
            
            if no == 100:
                break;
            
    except Exception as e:        
        print('예외가 발생했습니다.', e)
        return "false"

    return "true"
        


# table 생성
def create_region_data():
    global conn, cur

    try:
        conn.execute('CREATE TABLE naver_land_region(id INTEGER, cortarNo TEXT, cortarName TEXT, centerLat TEXT, centerLon TEXT, cortarType TEXT) ')
        
    except Exception as e:
        print('예외가 발생했습니다.', e)
        return False

    return True

# db연결
def conn_region_data():
    global no, conn, cur
    no = 0

    try:
        conn = sqlite3.connect("naver_land.db")
        cur = conn.cursor()
    except Exception as e:
        conn.close()
        print('예외가 발생했습니다.', e)
        return False

    return True

# 연결해제
def close_region_data():
    global no, conn, cur

    try:
        conn.close()
    except Exception as e:
        conn.close()
        print('예외가 발생했습니다.', e)
        return False

    return True


# HTTP Server
host_addr = "localhost"
port_num = "8080"
app = Flask(__name__)

@app.route("/region_root")
def get_region_root_search():
    now = datetime.datetime.now()
    print('>>>>>>>>>>>>>> start time [get_region_root_search] : '+ str(now))

    conn_region_data()
    create_region_data()
    result = get_land_region_root()
    close_region_data()

    now = datetime.datetime.now()
    print('>>>>>>>>>>>>>> end time [get_region_root_search] : '+str(now))
    return result

@app.route("/region_area")
def get_region_area():
    now = datetime.datetime.now()
    print('>>>>>>>>>>>>>> start time [get_region_area] : '+ str(now))
    conn_region_data()
    result = select_land_region()
    close_region_data()

    now = datetime.datetime.now()
    print('>>>>>>>>>>>>>> end time [get_region_area] : '+str(now))
    return result

if __name__ == "__main__":

    app.run(host=host_addr, port=port_num)



