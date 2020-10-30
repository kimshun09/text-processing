# coding: UTF-8

#wikiデータが格納されたデータベースをもとにMeCabを用いて形態素解析し，固有名詞のみを取り出してファイル出力する

import MeCab
import sqlite3
import os
import codecs

wiki = 100
dbfile = '../database/wiki' + str(wiki) + '.db'
rawfile = '../tmp/rawwords' + str(wiki) + '.txt'

m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/ipadic")

if os.path.exists(dbfile) == False:
    print(dbfile + ' doesn\'t exist')
    exit()
if os.path.exists(rawfile) == True:
    print(rawfile + ' already exists.')
    yesno = input('continue? (yes/no): ')
    if yesno != 'yes':
        exit()

conn = sqlite3.connect(dbfile)
c = conn.cursor()
bodies = c.execute('select BODY from ARTICLES')

f = codecs.open(rawfile, 'w', 'utf-8')

#データベースから1記事ずつ取り出しMeCabで形態素解析する
#固有名詞のみを取り出しファイルに出力する
#索引間はコンマで，記事間は改行で区別する
wordcount = 1
bodycount = 0
for body in bodies:
    text = m.parse(body[0])
    lines = text.split('\n')
    for line in lines:
        if line=='EOS':
            f.write(line)
            continue
        if line=='':
            f.write('\n')
            continue
        text = line.split('\t')
        parts = text[1].split(',')
        if parts[1]=='固有名詞':
            f.write(text[0] + ',')
            print(wordcount)
            wordcount += 1
    bodycount += 1
print('bodycount:' + str(bodycount))

conn.close()
f.close()