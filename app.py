from flask import Flask, render_template
import re
import requests
import os
import datetime
import json
from bs4 import BeautifulSoup
from _collections import OrderedDict


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello 2weeks!!!!!!!!!!!!!'

@app.route('/crawling/image/<appName>/<keyword>/<num>', methods = ['GET'])
def crawling(keyword, num, appName):
    crawlingData = getImage(keyword, int(num), appName)
    return crawlingData


def getImage(keyword,num, appName):

    #키워드 스플릿
    keyword.replace(" ", "")
    splitKeywords = keyword.split(',')

    # 이미지 파일 경로 및 파일 이름 저장
    fileData = OrderedDict()

    for j in range(len(splitKeywords)):

        url="https://search.naver.com/search.naver?where=image&sm=tab_jum&query="+splitKeywords[j]
        html = requests.get(url)
        bs_html = BeautifulSoup(html.content,"html.parser")
        photowall = bs_html.find('div',{"class":"photowall"})
        img_list = photowall.find_all("img",{"class":"_img"})

        DIR = "../data" + makeSaveFilePath(appName)

        #폴더가 없을 경우 폴더 생성
        if not os.path.exists(DIR):
                #여러개의 폴더를 한번에 생성해줌
                os.makedirs(DIR, exist_ok=True)

        #파일 이름 세팅
        basename = "crawImg"
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = "_".join([basename, suffix])


        filePathList = []
        #폴더에 이미지 다운로드
        for i in range(num):
            img_link = re.findall('data-source="(.+?)"',str(img_list[i]))[0]
            img_con = requests.get(img_link).content

            filePath = DIR+"/" + filename + "_" + str(j) + str(i+1) + ".jpg"
            filePathList.append(filePath)

            file = open(filePath,"wb")
            file.write(img_con)
            file.close()

        fileData[splitKeywords[j]] = filePathList

    return fileData

def makeSaveFilePath(appName):
    today = datetime.datetime.today()
    path = "/" + appName + "/" + str(today.year) + "/" + str(today.month) + "/" + str(today.day)
    return path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
