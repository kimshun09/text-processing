# coding: UTF-8

#各記事ごとに形態素解析して取り出した索引語をもとにTFを計算しファイル出力する

import codecs
import os
import collections

wiki = 100
rawfile = '../tmp/rawwords' + str(wiki) + '.txt'
termsfile = '../tmp/tf' + str(wiki) + '.txt'

if os.path.exists(rawfile) == False:
    print(rawfile + ' does\'nt exist')
    exit()
if os.path.exists(termsfile) == True:
    print(termsfile + ' already exists.')
    yesno = input('continue? (yes/no): ')
    if yesno != 'yes':
        exit()

fr = codecs.open(rawfile, 'r', 'utf-8')
fw = codecs.open(termsfile, 'w', 'utf-8')

#単語のファイルを1記事ずつつまり1行ずつ読み込み，TFを計算する
#'索引語:TF値'のようにファイル出力する
#索引語間はコンマで，記事間は改行で区別する
lines = fr.read().split('\n')[:-1]
for i, line in enumerate(lines):
    terms = line.split(',')
    if len(terms) == 1:
        fw.write(' \n')
        continue
    terms = terms[:-1]
    #ディクショナリを用いる
    dic = collections.Counter(terms)
    sum = 0
    for freq in dic.values():
        sum += freq
    l = ''
    for term, freq in dic.items():
        l += term+':'+str(freq/sum)+','
    l = l[:-1]+'\n'
    fw.write(l)
    print(i+1)

fr.close()
fw.close()