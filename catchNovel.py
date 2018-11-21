#coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
from urllib import error
import http.client
import time

#解决http.client.IncompleteRead: IncompleteRead(0 bytes read错误"
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
#小说地址
novel_url = "http://www.biqukan.com/2_2537/"
#小说内容前半部分地址
content_base_url = "http://www.biqukan.com"
#小说保存的路径
novel_dir = 'MyNovel/'
#https请求头
headers = {
    'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/70.0.3538.77 Safari/537.36',
    'Connection': 'keep-alive'
}


#获取所有章节的url和title
def get_url_title():
    try:
        chapter_request = urllib.request.Request(novel_url, headers=headers)
        chapter_response = urllib.request.urlopen(chapter_request)
        chapter_content = chapter_response.read()
        #使用BeautifulSoup
        chapter_beautiful_soup = BeautifulSoup(chapter_content, 'html.parser')
        all_chapter = chapter_beautiful_soup.find_all(attrs={"class": "listmain"})
        list_a = []
        for i in all_chapter:
            for j in i.find_all('a'):
                list_a.append(j)
        #去掉不需要的<a>...</a>
        url_title_list = list_a[12:]
        return url_title_list
    except error.URLError as reason:
            print(str(reason))


#下载小说
def down_navel_content(url_title):
    #拼接每章的url
    contents_url = content_base_url+url_title.attrs.get('href')
    #每获取章节名字
    content_title = url_title.string
    try:
        chapter_request = urllib.request.Request(contents_url, headers=headers)
        chapter_response = urllib.request.urlopen(chapter_request)
        chapter_content = chapter_response.read()
        #使用BeautifulSoup
        chapter_beautiful_soup = BeautifulSoup(chapter_content, 'html.parser')
        #获取小说内容
        contents = chapter_beautiful_soup.find_all(attrs={"class": "showtxt"})
        for txt in contents:
            save_navel(txt, novel_dir+content_title+'.txt')
    except error.URLError as reason:
            print(str(reason))


#保存小说
def save_navel(content, path):
    try:
        #设置编码方式为utf-8
        with open(path, 'w+', encoding='utf-8')as f:
            #get_text(strip=True)是去掉空格和换行
            f.write(content.get_text(strip=True))
    except error.URLError as reason:
            print(str(reason))
    else:
        print('下载完'+path)


if __name__ == '__main__':
    novel_chapter = get_url_title()
    for chapter in novel_chapter:
        down_navel_content(chapter)
        time.sleep(10);
    print('全部下载完成')