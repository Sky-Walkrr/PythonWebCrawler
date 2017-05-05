# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import re


def request1():
    r = requests.get("http://www.cuiqingcai.com")
    print type(r)
    print r.status_code
    print r.encoding
    print r.cookies


def request2():
    payload = {'key1': 'value1', 'key2': 'value2'}
    header = {
        'user-agent': 'Mozilla',
        'content-type': 'application/json'
    }
    r = requests.post('http://httpbin.org/post', data=payload)  # 一个神奇的站点～
    print r.text


def request3():
    s = requests.Session()
    s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')  # session创建会话
    r = s.get("http://httpbin.org/cookies")
    print(r.text)


def request4():
    r = requests.get('https://kyfw.12306.cn/otn/', verify=True)
    print r.text


def request5():
    proxy = {
        'https': 'http://41.118.132.69:4433'
    }
    r = requests.get('http://httpbin.org/get', proxies=proxy)  # try this may be interesting: r = requests.get('http://httpbin.org/post', proxies=proxy)
    print r.status_code
    print r.text


def bs():
    html = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
    <a href="http://example.com/lacie" class="brother" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
    <p class="story">...</p>
    """

    soup = BeautifulSoup(html, 'html.parser')  # define a parser :-)
    print soup.prettify()
    print soup.p
    print soup.body
    print soup.name
    print soup.p.name
    print soup.attrs
    print soup.p.attrs
    print soup.p['name']  # soup.p.get('name')

    print soup.p.string
    print type(soup.p.string)
    print type(soup.a.string)

    print soup.body.contents[1]
    for child in soup.body.children:
        print child

    for child in soup.descendants:
        print child

    print soup.find_all('a')[0]
    for item in soup.find_all(re.compile(r'^b')):
        print item
        print '\n'

    def has_class_but_no_id(tag):
        return tag.has_attr('class') and not tag.has_attr('id')  # has_attr是element的方法。。。
    print soup.find_all(has_class_but_no_id)  # find_all可以传函数的用例，注意传的函数不须带参数

    print soup.find_all('a', class_='sister')  # 解决预留关键字冲突的方法
    print soup.find_all('a', attrs={'class', 'sister'})  # 这种方法页可以的哈哈

    # css 选择器--------------------------------------------------------------------------------

    print soup.select('#link1')
    print soup.select('.brother')
    print soup.select('body')
    for item in soup.select('body > p'):  # 父子节点用'>'连接，注意前后带空格
        print item
        print '\n'
    print soup.select('p .brother')  # 不在同一节点；tag直接书写，类前面加'.',id前面加'#'
    for item in soup.select('title'):
        print item.get_text()  # get_text()也是bs4.element的方法


def selenium():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    chrome = webdriver.Chrome()
    chrome.get("http://www.python.org")
    assert 'Python' in chrome.title
    element = chrome.find_element_by_name('q')  # this is the name of search bar in python official page
    element.send_keys('pycon')  # simulate inputting
    element.send_keys(Keys.RETURN)
    print chrome.page_source

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# unit test in Python
class PythonOrgSearchTest(unittest.TestCase):  # inherit
    def setUp(self):
        self.drive = webdriver.Chrome()

    def test_python_org_search(self):
        drive = self.drive
        drive.get("http://www.python.org")
        assert 'Python' in drive.title
        element = drive.find_element_by_name('q')
        element.send_keys('pycon')
        element.send_keys(Keys.RETURN)
        print drive.page_source

    def tearDown(self):
        self.drive.close()

if __name__ == '__main__':
    unittest.main()


