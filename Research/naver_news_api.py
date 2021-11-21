import os
import sys
import re
import datetime
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

def get_search_count(query, display):
    query_text = urllib.parse.quote(query)
    url = "https://openapi.naver.com/v1/search/news.json?query=" + query_text

    # http request
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    # http response
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode('utf-8'))

        print('Last build date : ' + str(response_body_dict['lastBuildDate']))
        print('Total : '+ str(response_body_dict['total']))
        print('Start : '+ str(response_body_dict['start']))
        print('Display : '+ str(response_body_dict['display']))
        
        if response_body_dict['total'] == 0:
            search_count = 0
        else:
            search_total = math.ceil(response_body_dict['total'] / int(display))

            if search_total >= 10:
                search_count = 10
            else:
                search_count = search_total
            
            print('Search Total : '+ str(search_total))
            print('Search Count : ' + str(search_count))
    
    return search_count

def get_search_post(query, display, start, sort):
    global no, cur
    query_text = urllib.parse.quote(query)

    url = "https://openapi.naver.com/v1/search/news.json?query=" + query_text + "&display=" + str(display) + "&start=" + str(start) + "&sort=" + sort

    # http request
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    # http response
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode('utf-8'))
        for item_index in range(0, len(response_body_dict['items'])):
            try:
                remove_html_tag = re.compile('<.*?>')
                title = re.sub(remove_html_tag, '', response_body_dict['items'][item_index]['title'])
                originallink = response_body_dict['items'][item_index]['originallink'].replace("amp;", "")
                link = response_body_dict['items'][item_index]['link'].replace("amp;", "")
                description = re.sub(remove_html_tag, '', response_body_dict['items'][item_index]['description'])
                pubDate = response_body_dict['items'][item_index]['pubDate']
                contents = ""
                
                no += 1
                post_code = requests.get(link, headers=headers)
                post_text = post_code.text
                post_soup = BeautifulSoup(post_text, 'html.parser')
                
                if link.find('news.naver.com') > 0:
                    print('------------------------- detail[news.naver.com] start----------------------------------')
                    #print("내용 : " + post_soup.select("#articleBodyContents")[0].get_text())
                    #print('--------------------------detail[news.naver.com]  end---------------------------------')
                else:
                    print('------------------------- detail[etc] start----------------------------------')
                    #print('--------------------------detail[etc] end---------------------------------')
                """
                print('-----------------------------------------------------------')
                print("#" + str(no)) 
                print("Title : " + title)
                print("originallink : "+ originallink)
                print("Link : "+ link)
                print("Description : " + description)
                print("Pub Date : " + pubDate)
                print('-----------------------------------------------------------')
                """
            except:
                item_index += 1
            
            cur.executemany('INSERT INTO naver_data VALUES (?, ?, ?, ?, ?, ?, ?) ',
                            [(no, title, originallink, link, description, pubDate, contents)]
                            )

def get_root_search(query):
    global no, cur
    no = 0
    # 출력건수 (1~100)
    display = 10
    start = 1
    sort = 'date'
    now = datetime.datetime.now()
    print('>>>>>>>>>>>>>> start time : '+ str(now))
    startDate = now.strftime('%Y-%m-%d-%H-%M-%S')

    try:
            
        conn = sqlite3.connect(query+"_"+startDate+".db")
        conn.execute('CREATE TABLE naver_data(id INTEGER, title TEXT, originallink TEXT, link TEXT, description TEXT, pubdate TEXT, contents TEXT) ')
        cur = conn.cursor()
        
        search_count = get_search_count(query, display)
        for start_index in range(start, search_count + 1, display):
            get_search_post(query, display, start_index, sort)

        conn.commit()
        conn.close()
        now = datetime.datetime.now()
        print('>>>>>>>>>>>>>> end time : '+str(now))
    except Exception as e:
        conn.close()
        print('예외가 발생했습니다.', e)
        return "false"

    return "true"

# HTTP Server
host_addr = "localhost"
port_num = "8080"
app = Flask(__name__)

@app.route("/<query>")
def get_news_search(query):
    print(">>>>>>>>>>>>>>>>>> 검색어 : " + query)
    return get_root_search(query)

if __name__ == "__main__":
    app.run(host=host_addr, port=port_num)

