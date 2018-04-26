from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from threading import Thread
from selenium import webdriver
from lxml import etree
import urllib.request as request
import requests
import threading
import csv
import time
import sys
import os
import re

# 一级页面
def getPage(url, header):
    response = request.Request(url, headers=header)
    html = request.urlopen(response, None, 30).read().decode('utf-8')
    return html

def getURLs(html, host):
    urls = re.findall(r'href="(.*?)"', html)
    res = []
    for url in urls:
        if not url.endswith('css') and url.startswith('/zhuanti/') or url.endswith('/110002.html'):
            res.append(host + url)
    return res

# 二级页面
def cityURLs(url, host, header):
    driver = webdriver.Firefox()
    driver.get(url)
    '''单个城市'''
    try:
        element = driver.find_element_by_xpath("//a[contains(text(), '更多>>')]")
        suburl = element.get_attribute('href')
        page = getPage(suburl, header)
        element.click()
    except NoSuchElementException:
        driver.close()
        return False
    else:
        subpage = re.findall(r'<div class="wai">\r\n(.+?)</table>', page, re.S)
        tmp = re.findall(r'href="(.*?)"', subpage[0].strip())
        urls = []
        for i in tmp:
            if i.startswith('/chinese/home/docView/'):
                urls.append(host + i)
        while True:
            try:
                element = driver.find_element_by_xpath("//a[contains(text(), '下页')]")
            except NoSuchElementException:
                driver.close()
                return urls
            else:
                suburl = element.get_attribute('href')
                page = getPage(suburl, header)
                element.click()
                subpage = re.findall(r'<div class="wai">\r\n(.+?)</table>', page, re.S)
                tmp = re.findall(r'href="(.*?)"', subpage[0].strip())
                for i in tmp:
                    if i.startswith('/chinese/home/docView/'):
                        urls.append(host + i)

def chineseURLs(url, host, header):
    driver = webdriver.Firefox()
    driver.get(url)
    page = getPage(url,header)
    subpage = re.findall(r'<div class="wai">\r\n(.+?)</table>', page, re.S)
    tmp = re.findall(r'href="(.*?)"', subpage[0].strip())
    urls = []
    for i in tmp:
        if i.startswith('/chinese/home/docView/'):
            urls.append(host + i)
    while True:
        try:
            element = driver.find_element_by_xpath("//a[contains(text(), '下页')]")
        except NoSuchElementException:
            driver.close()
            return urls
        else:
            suburl = element.get_attribute('href')
            page = getPage(suburl, header)
            element.click()
            subpage = re.findall(r'<div class="wai">\r\n(.+?)</table>', page, re.S)
            tmp = re.findall(r'href="(.*?)"', subpage[0].strip())
            for i in tmp:
                if i.startswith('/chinese/home/docView/'):
                    urls.append(host + i)

def provinceURLsLocal(url, host, header):
    driver = webdriver.Firefox()
    driver.get(url)
    '''省级-银监局'''
    try:
        element = driver.find_element_by_id('ju_1')
        ActionChains(driver).move_to_element(element).perform()
        element = driver.find_element_by_xpath("//a[contains(text(), '更多>>')]")
        suburl = element.get_attribute('href')
        page = getPage(suburl, header)
        element.click()
    except NoSuchElementException:
        driver.close()
        return False     
    else:
        subpage = re.findall(r'<div class="wai">\r\n(.+?)</table>', page, re.S)
        tmp = re.findall(r'href="(.*?)"', subpage[0].strip())
        urls = []
        for i in tmp:
            if i.startswith('/chinese/home/docView/'):
                urls.append(host + i)
        while True:
            try:
                element = driver.find_element_by_xpath("//a[contains(text(), '下页')]")
            except NoSuchElementException:
                driver.close()
                return urls
            else:
                suburl = element.get_attribute('href')
                page = getPage(suburl, header)
                element.click()
                subpage = re.findall(r'<div class="wai">\r\n(.+?)</table>', page, re.S)
                tmp = re.findall(r'href="(.*?)"', subpage[0].strip())
                for i in tmp:
                    if i.startswith('/chinese/home/docView/'):
                        urls.append(host + i)
        


def retriveHTML(url, header, datafile, specialurl):
    '''分两种情况'''
    threadLock.acquire()
    time.sleep(1)
    page = getPage(url, header)
    pagepart = re.findall(r'.+?(<table class=Mso.*?</table>).*?', page, re.S)
    if pagepart:
        bs = BeautifulSoup(pagepart[0], 'html.parser')
        tmp = bs.find_all('td')
        if tmp:
            for i,each in enumerate(tmp):
                data = each.text.replace(' ', '').replace('\n','').strip()
                if "名称" == data or "主要负责人" in data or "案由" in data or "依据" in data or "行政处罚决定" == data or "日期" in data:
                    datafile.write("%s,"%tmp[i+1].text.replace(' ', '').replace('\n', ''))
            datafile.write('\n')
        else:
            print(url)
            specialurl.append(url)
    else:
        print(url)
        specialurl.append(url)
    threadLock.release()

def multiThread(urlset, header, datafile):
    threads = []
    specialurl = []
    for i in urlset:
        t = Thread(target=retriveHTML, args=(i, header,datafile, specialurl))
        threads.append(t)
    for j,each in enumerate(threads):
        threads[j].start()
    for j,each in enumerate(threads):
        threads[j].join()
    with open('unopenurl.csv', 'a') as unurlfile:
        for i in specialurl:
            unurlfile.write('%s\n'%i)
    unurlfile.close()
    

threadLock = threading.Lock()

if __name__ == "__main__":
    specialurl = [
        'http://www.cbrc.gov.cn/chinese/home/docView/752093D2E8C0479BB100DDEB8A4342A1.html'
    ]
    host = 'http://www.cbrc.gov.cn'
    initial_url = 'http://www.cbrc.gov.cn/forwardToXZCFPage2.html'
    header = {
        'Cookie': 'JSESSIONID=0000xCxEmgHwVDjuOg5dnYC6HeU:-1; __jsluid=bd3cf57c9895675187fa52972f2ec42f',
        'Referer': 'http://www.cbrc.gov.cn/forwardToXZCFPage2.html',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }
    with open('data.csv', 'a') as datafile:
        initial_html = getPage(initial_url, header)
        wait_queue = getURLs(initial_html, host)
        urls = set()
        for item in wait_queue:
            urlpart = cityURLs(item, host, header)
            if urlpart != False:
                urls.update(urlpart)
                multiThread(urlpart, header, datafile)
                urlpart = provinceURLsLocal(item, host, header)
                if urlpart != False:
                    urls.update(urlpart)
                    multiThread(urlpart, header, datafile)
            else:
                urlpart = chineseURLs(item, host, header)
                urls.update(urlpart)
                multiThread(urlpart, header, datafile)
    datafile.close()