# -*-coding:utf-8-*-
import urllib2
import re


class BDTB:
    def __init__(self, see_lz):
        self.base_url = "http://tieba.baidu.com/p/3138733512"
        self.see_lz = "?see_lz=" + str(see_lz)
        self.tool = Tool()

    def get_data(self, page):
        url = self.base_url + self.see_lz + "&pn=" + str(page)
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request).read()
            pattern_title = re.compile(r'core_title.*?title="(.*?)"', re.S)
            pattern_page_info = re.compile(r'l_reply_num.*?<span.*?>(.*?)<.*?>(.*?)<span.*?>(.*?)</.*?>(.*?)</.*?', re.S)
            pattern_contents = re.compile(r'class="d_post_content j_d_post_content.*?>(.*?)</div.*?<span class="tail-info">(.*?)<', re.S)
            print '帖子标题：', re.search(pattern_title, response).group(1), '\n'
            page_info = re.search(pattern_page_info, response)
            print page_info.group(1), page_info.group(2), page_info.group(3), page_info.group(4), '\n'
            contents = re.findall(pattern_contents, response)
            for content in contents:
                print content[1], '----------------------------------------------------------------\n'
                content = self.tool.clean(content[0])
                print content, '\n'

        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print '--> url error ' + str(e.code)
            if hasattr(e, 'reason'):
                print '--> url error ' + e.reason


# 处理文本工具类
class Tool:
    def __init__(self):
        # 图片标签
        self.p_img = re.compile(r'<img.*?>')
        # 换行符
        self.p_br = re.compile(r'<br><br>|<br>')
        # 超链接
        self.p_link = re.compile(r'<a.*?>|</a>')
        # 制表符
        self.p_tab = re.compile(r'<td>')
        # 段落
        self.p_para = re.compile(r'<p.*?>')
        # 空格
        self.p_blank = re.compile(r' {7}')

    def clean(self, content):
        content = re.sub(self.p_img, '', content)
        content = re.sub(self.p_br, '\n', content)
        content = re.sub(self.p_link, '', content)
        content = re.sub(self.p_blank, '', content)
        return content.strip()

spider = BDTB(1)
spider.get_data(1)
