# coding: UTF-8

#TFファイルをもとにIDFを計算しファイル出力する

import codecs
import os
import math
import time

wiki = 100
tffile = '../tmp/tf' + str(wiki) + '.txt'
idffile = '../tmp/idf' + str(wiki) + '.txt'

if os.path.exists(tffile) == False:
    print(tffile + ' doesn\'t exist')
    exit()
if os.path.exists(idffile) == True:
    print(idffile + ' already exists.')
    yesno = input('continue? (yes/no): ')
    if yesno != 'yes':
        exit()


fr = codecs.open(tffile, 'r', 'utf-8')
fw = codecs.open(idffile, 'w', 'utf-8')

#TFファイルを改行，コンマで区切り索引語行列つまり2次元配列をつくる
articles = fr.read().split('\n')[:-1]
termlists = [ [articles[i].split(',')[j].split(':')[0] for j in range(len(articles[i].split(',')))]
              for i in range(len(articles)) ]

#索引語行列から重複を除き，索引語リストをつくる
idf = []
for l in termlists:
    idf.extend(l)
idf.remove(' ')
idf = dict.fromkeys(idf, 0)

start = time.time()

#索引語行列，索引語リストをもとにIDFを計算する
#'索引語:IDF値'のように1行ずつファイル出力する
for i, term in enumerate(idf):
    count = 0
    for termlist in termlists:
        if term in termlist:
            count += 1
    idf[term] = math.log(len(articles)/count) + 1
    fw.write(term + ":" + str(idf[term]) + '\n')
    end = time.time()
    p = (i+1) / len(idf) * 100
    prcstime = (end - start) / 60
    estmtime = (len(idf)-(i+1)) / ((i+1)/(end-start)) / 60
    print(f'{p:5f}%, {prcstime:5f}min passed, {estmtime:5f}min to go')


fr.close()
fw.close()



