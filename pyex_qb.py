# -*-coding:utf-8-*-
# 抓取糗事百科网站热门数据并筛选处理的简单爬虫
import urllib2
import re


class QB:
    # 定义初始化变量
    def __init__(self):
        self.page = 1
        self.enable = False
        self.url = "http://www.qiushibaike.com/hot/page/"
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
        self.pages = []  # 存放爬取的数据页

    def get_page_items(self, page):
        self.page = page
        request = urllib2.Request(self.url + str(self.page))  # 处理分页
        request.add_header('user-agent', self.user_agent)
        try:
            response = urllib2.urlopen(request).read()
            print '请求加载数据，url: ', request.get_full_url()
            pattern = re.compile(r'<div.*?author.*?title="(.*?)".*?<div.*?content.*?<span>(.*?)</span>(.*?)stats.*?'
                                 r'stats-vote.*?number">(.*?)</i>(.*?)<.*?stats-comment.*?number">(.*?)</i>(.*?)<',
                                 re.S)  # 注意\w匹配汉字的问题；还有.默认不匹配换行符，但抓取的html换行，需要指定flag
            items = re.findall(pattern, response)
            page_items = []  # 存放每页的条目
            for item in items:  # 这里用finditer遍历无法取到单个元素？
                # 过滤带图的帖子
                if not re.search("thumb", item[2]):  # search 接收string或者buffer,不能直接传item
                    content_text = re.sub(re.compile(r'<br/>'), '\n', item[1])  # content有些含有<br/>,转为\n换行
                    page_item = [item[0], content_text, item[3], item[4], item[5], item[6]]
                    page_items.append(page_item)
            # print str(page_items[2]).decode('string_escape')  # 解决打印list中文变unicode问题
            return page_items

        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print '-->error: error code', e.getCode()
            if hasattr(e, 'reason'):
                print '--> error: error reason', e.getReason()

    def load_page(self):
        if self.enable:
            # 未读页小于2自动加载下一页
            if len(self.pages) < 2:
                self.pages.append(self.get_page_items(self.page))
                self.page += 1

    def print_one_post(self, page_items, page):
        # 遍历一页的数据条目
        for item in page_items:
            user_input = raw_input()
            self.load_page()
            if user_input == 'Q':
                self.enable = False
                return
            print "第%d页\t发帖人：%s\n帖子:\n%s\n" % (page, item[0], item[1])
            print item[2], item[3], item[4], item[5]

    def start(self):
        print 'start clawing,pls wait.input Q to exit'
        self.enable = True
        self.load_page()
        now_page = 0
        while self.enable:
            if len(self.pages) > 0:
                now_page += 1
                self.print_one_post(self.pages[0], now_page)
                del self.pages[0]

qb_spider = QB()
qb_spider.start()

