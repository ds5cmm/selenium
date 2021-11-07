import os
import sys
import re
import datetime
import math
import json
import requests
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

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
    global no, fs
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

                no += 1
                print('-----------------------------------------------------------')
                print("#" + str(no)) 
                print("Title : " + title)
                print("originallink : "+ originallink)
                print("Link : "+ link)
                #print("Description : " + description)
                print("Pub Date : " + pubDate)
                print('-----------------------------------------------------------')
                if link.find('news.naver.com') > 0:
                    post_code = requests.get(link, headers=headers)
                    
                    post_text = post_code.text
                    post_soup = BeautifulSoup(post_text, 'html.parser')
                    print('------------------------- detail start----------------------------------')                
                    
                    fs.write("번호 : " + str(no) + "\n")
                    fs.write("제목 : " + post_soup.select("#articleTitle")[0].text + "\n")
                    fs.write("게시일자 : " + pubDate + "\n")
                    fs.write("내용 : " + post_soup.select("#articleBodyContents")[0].get_text())

                    print('--------------------------detail end---------------------------------')


            except:
                item_index += 1

if __name__ == '__main__':
    no = 0
    # 검색어
    query = "오징어게임"
    # 출력건수 (1~100)
    display = 100
    start = 1
    sort = 'date'

    fs = open(query +".txt", 'w', encoding='utf-8')

    search_count = get_search_count(query, display)
    for start_index in range(start, search_count + 1, display):
        get_search_post(query, display, start_index, sort)

    fs.close()

    