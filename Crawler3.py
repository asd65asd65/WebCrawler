
import requests
from bs4 import BeautifulSoup
import time
import re
#import numpy as np
import pandas as pd
import json

def title():
    print('*-----搜尋參數-----*')
    a = searchpage.title
    print(a.string)
    print(' ')
    
    print('*-----搜尋結果-----*')
    span_tags = searchpage.select("div.r > a > h3 > span.S3Uucc", limit = maxnumber)
    i = 0
    for tag in span_tags:
        i=i+1
        print(i,".",tag.string)
    print(' ')
    time.sleep(1)
    print('*-----搜尋結果解析START-----*')
    print(' ')

def addDataToJson(jsonfile, index, totlescore):
    df2 = {"name":df["目標"][index], "introduction":df["簡介"][index],
           "score":totlescore}    
    with open(jsonfile, 'a') as fp:
        fp.write(json.dumps(df2, ensure_ascii=False)+"\n")
        fp.close

def addDataToJson2(jsonfile, index, totlescore):
    df2 = {"name":df["name"][index], "introduction":df["introduction"][index], 
       "open_time":df["open_time"][index], "address":df["address"][index], 
       "lat":df["lat"][index], "long":df["long"][index], "score":totlescore}    
    with open(jsonfile, 'a') as fp:
        fp.write(json.dumps(df2, ensure_ascii=False)+"\n")
        fp.close

# Google 搜尋 URL
url = "https://www.google.com.tw/search"

#模擬瀏覽器送出    
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108" 
           "Safari/537.36 Edge/18.17763"}

# 查詢設定
maxpage = 3
maxnumber = 10 # find limit every page
index = 0
#讀取檔案
df = pd.read_excel("成就表.xlsx")
print("分析開始")
jsonfile = "play4.json"
with open(jsonfile, 'w') as fp:
        fp.write("")
        fp.close
for keyword in df["目標"]:
    totlescore = 0
    page = 1
    # 查詢參數
    search = keyword
    my_params = {"q": search}
    for page in range(1, maxpage + 1): #搜尋頁面控制
        try:
            r = requests.get(url, params = my_params, headers = headers)
            time.sleep(0.001)
        except requests.exceptions.SSLError:
            break
        except requests.exceptions.TooManyRedirects:
            break
        except requests.exceptions.ConnectionError:
            break
        except requests.exceptions.ConnectTimeout:
            break
        except requests.exceptions.Timeout:
            break
        # 確認是否下載成功
        if r.status_code == requests.codes.ok:
            # 以 BeautifulSoup 解析 HTML 程式碼
            searchpage = BeautifulSoup(r.text, "lxml")
            a_tags = searchpage.select("div.r > a", limit = maxnumber)
            for tag in a_tags: #尋訪此頁網站
                try:
                    r = requests.get(tag.get("href"), headers = headers)
                except requests.exceptions.SSLError:
                    break
                except requests.exceptions.TooManyRedirects:
                    break
                except requests.exceptions.ConnectionError:
                    break
                except requests.exceptions.ConnectTimeout:
                    break
                except requests.exceptions.Timeout:
                    break
                #time.sleep(0.1)
                if r.status_code == requests.codes.ok:
                    web = BeautifulSoup(r.text, "lxml")
                    tags = web.find_all("p", string = re.compile(search))
                    for tag2 in tags: #尋訪網頁內容
                        totlescore = totlescore + 1
                    tags = web.find_all("span", string = re.compile(search))
                    for tag2 in tags: #尋訪網頁內容
                        totlescore = totlescore + 1
                else:
                    break
        else:
            break
        my_params = {"q": search, "start": page*10}
        print("累積分數: ", totlescore, " ->page: ", page, " ->->->nextpage")
        page = page + 1 #下一頁
    print(index, "", keyword, " -> 熱門度總分: ", totlescore) #總分統計
    addDataToJson(jsonfile, index, totlescore) # 新增資料
    index = index + 1
    if index >=200 :
        break
print("分析結束")
# 檔案輸出
print('*-----資料建立成功-----*')
with open(jsonfile, 'r') as fp2:
    print(fp2.read())