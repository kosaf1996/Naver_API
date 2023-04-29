from bs4 import BeautifulSoup as bs
from flask import Flask, render_template
import requests
import time

###################################################################
###                   Papago Class                             ###
###################################################################
class papago:
    #########################################
    ##            초기화 함수               ##
    #########################################
    def __init__(self):
        self.api_key_id = ""
        self.api_key = ""
        self.space = " "
        self.new_line = "\n"
        self.content = "application/x-www-form-urlencoded"

    #########################################
    ##             웹 크롤링                ##
    #########################################
    def Crawling(self):
        url = 'https://www.kdca.go.kr/contents.es?mid=a20108010000'

        response = requests.get(url)
        # if response.status_code == 200:
        #     html = response.text
        #     soup = bs(html, 'html.parser')    
        #     content = soup.select_one('#contentWrap') #content#content  '#content_detail > div:nth-child(3)' #content_detail > div:nth-child(5)
        #     #print(title)
        # else : 
        #     print(response.status_code)  #content_detail > div:nth-child(3)
        #     response = requests.get(url)
            
        #print(content.text)
        return papago.papago_translation(response)

    #########################################
    ##           papago 호출               ##
    #########################################
    def papago_translation(self, html):
        headers  = {
            'Content-Type': self.content,
            'X-NCP-APIGW-API-KEY-ID': self.api_key_id,
            'X-NCP-APIGW-API-KEY': self.api_key
        }
        data = {
            'source': 'ko',
            'target': 'en',
            'html': html
        }

        url = "https://naveropenapi.apigw.ntruss.com/web-trans/v1/translate"
        
        res = requests.post(url, headers=headers, data=data)
        #print("한국어 :",html)
        #print('영문 번역:',res.text)

        return papago.create_html(res.text)

    #########################################
    ##         index.html Create           ##
    #########################################
    def create_html(self, translation):
       filePath = 'C:\\Users\\GoodusData\\Desktop\\work\\99.code\\python\\papgo\\templates\\index.html'
       f = open(filePath, 'w', encoding='utf-8')
       f.write(translation)

#########################################
##            Flask Web                ##
#########################################
app = Flask(__name__)
@app.route('/')
def index():

    return render_template('index.html')

    #########################################
    ##              메인 함수               ##
    #########################################  
if __name__ == '__main__':
    papago = papago()
    papago.Crawling() 
    time.sleep(20)
    app.run(debug=True)

    