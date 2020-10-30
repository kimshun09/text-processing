# coding: UTF-8

#TF,IDFファイルを元にTFIDFを計算しファイル出力する．

import codecs
import os

wiki = 100
tffile = '../tmp/tf' + str(wiki) + '.txt'
idffile = '../tmp/idf' + str(wiki) + '.txt'
tfidffile = '../tmp/tfidf' + str(wiki) + '.txt'

if os.path.exists(tffile) == False:
    print(tffile + ' doesn\'t exist')
    exit()
if os.path.exists(idffile) == False:
    print(tffile + ' doesn\'t exist')
    exit()
if os.path.exists(tfidffile) == True:
    print(idffile + ' already exists.')
    yesno = input('continue? (yes/no): ')
    if yesno != 'yes':
        exit()

fr_t = codecs.open(tffile, 'r', 'utf-8')
fr_i = codecs.open(idffile, 'r', 'utf-8')
fw = codecs.open(tfidffile, 'w', 'utf-8')

#TFファイルを読み込み，要素がディクショナリであるリストに格納する
lines = fr_t.read().split('\n')[:-1]
tf = []
for line in lines:
    dic = {}
    if line == ' ':
        tf.append({' ':0})
        continue
    terms = line.split(',')
    for term in terms:
        parts = term.split(':')
        dic[parts[0]] = float(parts[1])
    tf.append(dic)

#IDFファイルを読み込み，ディクショナリに格納する
lines = fr_i.read().split('\n')[:-1]
idf = {}
for line in lines:
    parts = line.split(':')
    idf[parts[0]] = float(parts[1])

#TFIDF値を計算する
#'索引語:TFIDF値'のようにファイル出力する
#索引語間はコンマで，記事間は改行で区別する
for i, article in enumerate(tf):
    if article == {' ':0}:
        fw.write(' \n')
        continue
    line = ''
    for term, tfvalue in article.items():
        idfvalue = idf[term]
        tfidfvalue = tfvalue * idfvalue
        line += term + ":" + str(tfidfvalue) + ','
    line = line[:-1] + '\n'
    fw.write(line)
    print(i+1)


fr_t.close()
fr_i.close()
fw.close()



