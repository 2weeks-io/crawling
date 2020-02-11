from flask import Flask, render_template
import re
import requests
import os
import datetime
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello 2weeks!'

@app.route('/crawling/image/<keyword>/<num>', methods = ['GET'])
def crawling(keyword, num):
    getImage(keyword, int(num))
    return "crawling"


def getImage(keyword,num):
    url="https://search.naver.com/search.naver?where=image&sm=tab_jum&query="+keyword
    html = requests.get(url)
    bs_html = BeautifulSoup(html.content,"html.parser")
    photowall = bs_html.find('div',{"class":"photowall"})
    img_list = photowall.find_all("img",{"class":"_img"})

    DIR = "../search_img/"

    #폴더가 없을 경우 폴더 생성
    if not os.path.exists(DIR):
            os.mkdir(DIR)
        
    #파일 이름 세팅
    basename = "crawImg"
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([basename, suffix])

    #폴더에 이미지 다운로드
    for i in range(num):
        img_link = re.findall('data-source="(.+?)"',str(img_list[i]))[0]
        img_con = requests.get(img_link).content
        file = open(DIR+filename+"_"+str(i+1)+".jpg","wb")
        file.write(img_con)
        file.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, )
