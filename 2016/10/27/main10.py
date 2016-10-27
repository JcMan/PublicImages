# coding=utf-8
import requests,os,threading
import sqlite3
from bs4 import *


def getCursor():
    conn = sqlite3.connect('db')
    conn.isolation_level = None #隔离级别设置
    return conn.cursor()


def saveSrc(src,title):
    sql = "insert into src values('"+title+"','"+src+"')"
    getCursor().execute(sql)


def downImgs(href,title):
    html = requests.get(href).content
    soup = BeautifulSoup(html,'lxml')
    imgs = soup.find_all(class_="f14 mb10")[0].find_all('img')
    print href+title
    for img in imgs:
        src = img.get('src')
        saveSrc(src,title)


def showSrcs():
    sql = "select * from src"
    result = getCursor().execute(sql).fetchall()
    print result


def deleteSrcs():
    sql = "delete from src"
    getCursor().execute(sql)
    print "已删除"


def getTitles():
    sql = "select distinct title from src"
    result = getCursor().execute(sql).fetchall()
    return result

def getSrcsByTitle(title):
    sql = "select src from src where title = '"+title+"'"
    return getCursor().execute(sql).fetchall()


def downloadImg(title,srcs):
    print title
    dirpath = os.path.join(os.getcwd(),'img')
    dirpath = os.path.join(dirpath,title)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    count = len(srcs)
    for i in range(1,count,1):
        src = srcs[i][0]
        t = os.path.splitext(src)[1]
        path = os.path.join(dirpath,str(i)+t)
        if not os.path.exists(path):
            try:
                data = requests.get(src).content
                with open(path,"wb") as code:
                    code.write(data)
            except:
                pass


class DownLoad(threading.Thread):
    def __init__(self,start,end,titles):
        threading.Thread.__init__(self)
        self.s = int(start)
        self.e = int(end)
        self.titles = titles
    
    def run(self):
        for i in range(self.s,self.e+1,1):
            title = self.titles[i]
            print i
            srcs = getSrcsByTitle(title[0])
            downloadImg(title[0],srcs)


def saveImg():
    titles = getTitles()

    d4 = DownLoad(401,500,titles)
    d4.start()

    d5 = DownLoad(501,600,titles)
    d5.start()

    d6 = DownLoad(601,700,titles)
    d6.start()

    d7 = DownLoad(701,800,titles)
    d7.start()

    d8 = DownLoad(801,900,titles)
    d8.start()




if __name__ == '__main__':
    # showSrcs()
    # deleteSrcs()
    saveImg()
    # baseurl = 'http://x772816.net/bbs/thread.php?fid=57&page='
    # for i in range(50,556,1):
    #     url = baseurl+str(i)
    #     html = requests.get(url).content
    #     soup = BeautifulSoup(html,'lxml')
    #     tr3s = soup.find_all(class_="tr3")
    #     print i
    #     for tr in tr3s:
    #         subject = tr.find_all(class_="subject")[0].find_all('a')[0]
    #         href = "http://x772816.net/bbs/"+subject.get('href')
    #         title = subject.string
    #         downImgs(href,title)
