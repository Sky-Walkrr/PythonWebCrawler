from pyquery import PyQuery as pq


def pyex1():
    doc = pq(filename='sample.html')
    print doc.html()
    print type(doc)
    li = doc('li')
    print li.text()
    print type(li)


def pyex2():
    doc = pq('<p id="hello" class="hello"></p>')
    print doc.attr('id')
    print doc.attr('id', 'hi')
    print doc.attr('id', 'hello')
    print doc.add_class('guys')
    print doc.remove_class('hello')
    print doc.css('font-size', '16px')
    print doc.css('background', '#fff')

pyex2()
