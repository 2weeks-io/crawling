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

@app.route('/crawling/image/<appName>/<srchPrefix>/<keyword>/<num>', methods = ['GET'])
def crawling(keyword, num, appName, srchPrefix):
    crawlingData = getImage(keyword, int(num), appName, srchPrefix)
    return crawlingData

@app.route('/crawling2/image2/<appName>/<srchPrefix>/<keyword>/<num>', methods = ['GET'])
def crawling2(keyword, num, appName, srchPrefix):
    crawlingData = getImage2(keyword, int(num), appName)
    return crawlingData

def getImage(keyword,num, appName, srchPrefix):

    #키워드 스플릿
    keyword.replace(" ", "")
    splitKeywords = keyword.split(',')
    srchPrefix = srchPrefix + " "

    # 이미지 파일 경로 및 파일 이름 저장
    fileData = OrderedDict()

    for j in range(len(splitKeywords)):

        url="https://search.naver.com/search.naver?where=image&sm=tab_jum&query="+srchPrefix+splitKeywords[j]
        html = requests.get(url)
        bs_html = BeautifulSoup(html.content,"html.parser")
        photowall = bs_html.find('div',{"class":"photowall"})
        img_list = photowall.find_all("img",{"class":"_img"})

        #년월일시로 생성
        DIR = makeSaveFilePath()

        #폴더가 없을 경우 폴더 생성
        if not os.path.exists(DIR):
            print("/"+ appName+ DIR)
            #여러개의 폴더를 한번에 생성해줌
            os.makedirs("../data/"+ appName+ DIR, exist_ok=True)

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

            file = open("../data" + "/" + appName + filePath,"wb")
            file.write(img_con)
            file.close()

        fileData[splitKeywords[j]] = filePathList

    return fileData


def getImage2(keyword,num, appName, srchPrefix):

    #키워드 스플릿
    keyword.replace(" ", "")
    splitKeywords = keyword.split(',')
    srchPrefix = srchPrefix + " "

    # 이미지 파일 경로 및 파일 이름 저장
    fileData = OrderedDict()

    for j in range(len(splitKeywords)):

        url="https://search.naver.com/search.naver?where=image&sm=tab_jum&query="+srchPrefix+splitKeywords[j]
        html = requests.get(url)
        bs_html = BeautifulSoup(html.content,"html.parser")
        photowall = bs_html.find('div',{"class":"photowall"})
        img_list = photowall.find_all("img",{"class":"_img"})

        #년월일시로 생성
        DIR = makeSaveFilePath()

        #폴더가 없을 경우 폴더 생성
        if not os.path.exists(DIR):
            print("/"+ appName+ DIR)
            #여러개의 폴더를 한번에 생성해줌
            os.makedirs("../data/"+ appName+ DIR, exist_ok=True)

        #파일 이름 세팅
        basename = splitKeywords[j]
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        filename = basename


        filePathList = []
        #폴더에 이미지 다운로드
        for i in range(num):
            img_link = re.findall('data-source="(.+?)"',str(img_list[i]))[0]
            img_con = requests.get(img_link).content

            filePath = DIR+"/" + filename + "_" + str(j) + str(i+1) + ".jpg"
            filePathList.append(filePath)

            file = open("../data" + "/" + appName + filePath,"wb")
            file.write(img_con)
            file.close()

        fileData[splitKeywords[j]] = filePathList

    return fileData


def makeSaveFilePath():
    today = datetime.datetime.today()
    path = "/" + str(today.year) + "/" + str(today.month) + "/" + str(today.day)
    return path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
