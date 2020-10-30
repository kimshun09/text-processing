# coding: UTF-8

import codecs

f = codecs.open('../wiki/wiki100.txt', 'r', 'utf-8')
line = f.readline()
query = u'自然言語処理'

while line:
    start = article.find('\n') + 1
    end = start + article[start:].find('\n')
    word = article[start:end]
    if word.find(query) >= 0:
        print(article)
    line = f.readline()