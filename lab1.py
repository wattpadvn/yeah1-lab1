import requests
import json
import sys
import time
import sqlite3
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

###BROWSER INIITATE
def BR(URL):
	uAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1"
	session = requests.Session()
	session.headers.update({'User-Agent': uAgent})
	return session.get(URL)


### init browser and get cate ajax content and then return specify total page in each cate
def jCatPage(URL) :
    data = BR(URL).json()    
    last_page = data['paginator']['lastPage']
    total_news = data['paginator']['total']
    return last_page  ##INT

###build full urls list from cates
def buildcURLlist(cate) :
    NUM = '999999999' ###CONTS MAXXX NUMBER
    AjaxURL = 'https://yeah1.com/mb-load-more/{}?page={}' ###AJAX URL

    first_page = 1
    last_page = jCatPage(AjaxURL.format(cate, NUM))
    
    ###LIST URL
    urls = []

    for p in range(first_page, last_page) :
        print("request: {} | {}".format(cate, AjaxURL.format(cate,p)))
        ###Build all urls of each cate to list
        jContent = BR(AjaxURL.format(cate,p)).json()
        html = jContent['html']
        soup = BeautifulSoup(html, 'html.parser')
        
        ##get main div content and then get list of href
        divs = soup.findAll('div', attrs={'class' : 'card'}) 
        for div in divs:
            #print(div.a['href'])
            urls.append(div.a['href'])
        time.sleep(1)    
    print("build urls of {} completed".format(cate))
    return urls


'''
    get detail meta created_date, crawl_source from each post
    create_date : div class "card-meta"->span class "time"
    source_from: div class "article-content"->p class "text-right"
    title: class="card-title"
'''
def getDetail(cate) :
    urls = buildcURLlist(cate)
    for url in urls :         
        html = BR(url).content
        soup = BeautifulSoup(html, 'html.parser')
     
        ###TITLE        
        try :        
            title = soup.find('h1', {'class':'card-title'}).text
        except :
            title = 'yeah1'
        ###CREATED_DATE
        try :        
            div_time = soup.findAll('div', {'class': 'card-meta'})
            created_date = (div_time[0].find('span',{'class' : 'time'}).text.strip()).split(' ')[-1]
        except :
            created_date = 'yeah1'
                                
        ###CRAWL_SOURCE
        try :
            div_crawl = soup.findAll('div', {'class': 'article-content'})
                    
            if "text-right" in div_crawl[-1].text :
                crawl_source = div_crawl[-1].findAll('p',{'class':'text-right'})[-2].text.split('/')[-1]
            elif "Theo " in div_crawl[-1].text:
                crawl_source = div_crawl[-1].findAll('p')[-1].text.split('/')[-1]
            else :
                crawl_source =  "yeah1"            
        except :
            crawl_source =  "yeah1"
        #print ("title {} | url {} [created: {}] - [source: {}]".format(title, url, created_date, crawl_source))

        ####build list data
        data = [cate, title, url, "CONTENT", created_date, crawl_source]
        #print ("write data {} to DB".format(url))
        writedb(data)
        time.sleep(0.1)
    print("process completed {}".format(cate))

####Write post meta data to sqlitedb
def writedb(items) :    
    try:
        conn = sqlite3.connect('DB.db')        
        conn.execute("INSERT INTO detail (cate, title, url, content, created_date, crawl_source) VALUES(?,?,?,?,?,?)", (items))
        conn.commit()

    except sqlite3.Error as e:
        print('Error %s:' % e.args[0])
    finally:
        conn.close()

##Main func
def main() :
    CATES = ['photo-story', 'am-nhac', 'cong-dong-mang', 'cine', 'doi-song', 'check-in', 'dep', 'sao']
    ###fetch all from each cate
    for cate in CATES:
        getDetail(cate)

main()
