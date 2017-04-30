# -*-coding:utf-8-*-
import urllib2
import re


class BDTB:
    def __init__(self, base_url, see_lz):
        self.base_url = base_url  # https://tieba.baidu.com/p/5089994179
        self.see_lz = "?see_lz=" + str(see_lz)
        self.tool = Tool()

    def get_data(self, page):
        url = self.base_url + self.see_lz + "&pn=" + str(page)
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request).read()
            pattern_title = re.compile(r'core_title.*?title="(.*?)"', re.S)
            pattern_page_info = re.compile(r'l_reply_num.*?<span.*?>(.*?)<.*?>(.*?)<span.*?>(.*?)</.*?>(.*?)</.*?', re.S)
            pattern_contents = re.compile(r'class="d_post_content j_d_post_content.*?>([^(<div|</div)].*?)</div.*?<span class="tail-info">(\d+.*?)<', re.S)
            data = open('data.txt', 'a')  # a for append
            title = '帖子标题：' + re.search(pattern_title, response).group(1) + '\n'
            print '正在写入第%d页数据。。。' % page
            data.write(title)
            # print title
            page_info = re.search(pattern_page_info, response)
            page_data = page_info.group(1) + page_info.group(2) + page_info.group(3) + page_info.group(4) + '\n'
            # print page_data
            data.write(page_data)
            contents = re.findall(pattern_contents, response)
            content_data = []
            for content in contents:
                floor = content[1] + '----------------------------------------------------------------\n'
                print floor
                content_data.append(floor)
                content = self.tool.clean(content[0])
                # print content, '\n'
                content_data.append(content + '\n')
            for c in content_data:
                data.write(c)
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print '--> url error ' + str(e.code)
            if hasattr(e, 'reason'):
                print '--> url error ' + e.reason
        except IOError, e:
            if hasattr(e, 'code'):
                print '--> IO error ' + str(e.code)
            if hasattr(e, 'reason'):
                print '--> IO error ' + e.reason
        finally:
            data.close()

    def get_all_page(self):
        url = self.base_url + self.see_lz + "&pn=1"
        request = urllib2.Request(url)
        try:
            response = urllib2.urlopen(request).read()
            pattern_page_info = re.compile(r'l_reply_num.*?<span.*?>(.*?)<.*?>(.*?)<span.*?>(.*?)</.*?>(.*?)</.*?', re.S)
            page_info = re.search(pattern_page_info, response)
            page_count = int(page_info.group(3))
            print '该帖子共%s页' % page_count
            if page_count <= 1:
                self.get_data(1)
            else:
                for i in range(1, page_count + 1):  # 注意开闭区间的问题
                    self.get_data(i)

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


print '请输入需要抓取的帖子'
base_url = raw_input()
print '是否只看楼主？y/n'
if raw_input() == 'y':
    see_lz = 1
else:
    see_lz = 0
spider = BDTB(base_url, see_lz)
spider.get_all_page()
