# -*-coding:utf-8-*-
import os
from pyspider.libs.base_handler import *


START_PAGE = 1
END_PAGE = 2
DIR_PATH = '/Users/gchfeng/Documents/misc/temp'


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.base_url = 'https://mm.taobao.com/json/request_top_list.htm?page='
        self.page = START_PAGE
        self.total_page = END_PAGE
        self.tool = ImgTool()

    @every(minutes=24 * 60)
    def on_start(self):
        while self.page < self.total_page:
            url = self.base_url + str(self.page)
            print url
            self.crawl(url, callback=self.index_page)
            self.page += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.lady-name').items():  # 类前面加'.'
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        # 用pyspider的enable css selector mode简直不要太爽
        domain = 'http:' + response.doc('.mm-p-domain-info li > span').text()  # text 提取文本内容
        print domain
        self.crawl(domain, callback=self.domain_page, fetch_type='js')
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    def domain_page(self, response):
        name = response.doc('.mm-p-model-info-left-top dd > a').text()
        path = self.tool.make_dir(name)
        info = response.doc('.mm-aixiu-content').text()
        if path:
            imgs = response.doc('.mm-aixiu-content > div > img').items()  # multi-items
            self.tool.save_info(path, name, info)
            count = 1
            for img in imgs:
                url = img.attr.src
                if url:
                    img_name = name + str(count) + '.' + self.tool.get_suffix(url)
                    count += 1
                    self.crawl(url, callback=self.save_img, save={'path': path, 'name': img_name})

    def save_img(self, response):
        content = response.content
        path = response.save['path'] + '/' + response.save['name']
        self.tool.save_img(path, content)
        print '1 image saved successfully'


class ImgTool:
    def __init__(self):
        self.path = DIR_PATH
        if not self.path.endswith('/'):
            self.path += '/'
        if not os.path.exists(self.path):
            #  notice the difference between the mkdir() & makedirs()
            os.makedirs(self.path)

    def make_dir(self, name):
        path = self.path + name.strip()
        exist = os.path.exists(path)
        if not exist:
            os.makedirs(path)
        return path

    def save_img(self, path, img):
        f = open(path, 'wb')
        f.write(img)
        f.close()

    def save_info(self, path, name, content):
        file_path = path + '/' + name + '.txt'
        f = open(file_path, 'w+')  # w+ means read & write
        f.write(content.encode('utf-8'))  # encode
        f.close()

    def get_suffix(self, url):
        suffix = url.split('.')[-1]  # split() returns a list,and we need the last one element.
        return suffix

