# coding: UTF-8

import codecs
import time


f = codecs.open('../wiki/wiki100.txt', 'r', 'utf-8')
text = f.read()
f.close()
query = u'自然言語処理'
articles = text.split('</doc>')

t1 = time.time()
for article in articles:
    start = article.find('\n') + 1
    end = start + article[start:].find('\n')
    word = article[start:end]
    if word.find(query) >= 0:
        print(article)
t2 = time.time()
print(str(t2-t1) + ' sec')