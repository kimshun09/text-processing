# coding: UTF-8

#検索語から記事を1つ選び，その記事に類似する10記事をランキングで表示する

import codecs
import os
import sqlite3
import math
import sys

#検索語はコマンドライン引数から得る
keyword = sys.argv[1]

wiki = 100
dbfile = '../database/wiki' + str(wiki) + '.db'
tfidffile = '../tmp/tfidf' + str(wiki) + '.txt'

if os.path.exists(dbfile) == False:
    print(dbfile + ' doesn\'t exist')
    exit()
if os.path.exists(tfidffile) == False:
    print(tfidffile + ' doesn\'t exist')
    exit()

conn = sqlite3.connect(dbfile)
c = conn.cursor()

#TFIDFファイルの読み込み，要素がディクショナリであるリストに格納する
fr = codecs.open(tfidffile, 'r', 'utf-8')
lines = fr.read().split('\n')[:-1]
tfidf = []
for line in lines:
    dic = {}
    if line == ' ':
        tfidf.append({' ':0})
        continue
    terms = line.split(',')
    for term in terms:
        parts = term.split(':')
        dic[parts[0]] = float(parts[1])
    tfidf.append(dic)


#検索語から1つ記事を選ぶ
#まず見出し語が検索語と完全一致している記事を探す
#見つからなかった場合前方一致している記事を探す
#それでも見つからなかった場合は検索失敗とする
regex = (keyword + '\n',)
rowid = c.execute('select ROWID from ARTICLES where ENTRY like ?', regex)
fetch = rowid.fetchone()
if fetch == None:
    regex = (keyword + '%',)
    rowid = c.execute('select ROWID from ARTICLES where ENTRY like ?', regex)
    fetch = rowid.fetchone()
    if fetch == None:
        print('No articles found')
        exit()
id = fetch[0] - 1

#得られた記事のベクトルを検索語のベクトルとする
#固有名詞を含まず，TFIDFの値が1つもない記事の場合は失敗とする
vec = tfidf[id]
if vec == {' ', 0}:
    print('This keyword has no index terms and TF-IDF values.')
    exit()

#それぞれの記事のベクトルと検索後のベクトルとのcos類似度を計算しディクショナリとして格納
sml = {}
for i, article in enumerate(tfidf):
    dotpr = 0
    norm_v = 0
    norm_u = 0
    for term in vec.keys():
        dotpr += article.get(term, 0) * vec[term]
        norm_v += vec[term] ** 2
    for w in article.values():
        norm_u += w ** 2
    norm_v = math.sqrt(norm_v)
    norm_u = math.sqrt(norm_u)
    if dotpr != 0:
        value = dotpr / (norm_v * norm_u)
    else:
        value = 0
    sml[i] = value

#類似度でソートする
rank = sorted(sml.items(), key=lambda x:x[1], reverse=True)

#結果を表示する
#順位，索引語，類似度を表示する
for i in range(11):
    rowid = (rank[i][0]+1, )
    entry = c.execute('select ENTRY from ARTICLES where ROWID = ?', rowid)
    term = entry.fetchone()[0][:-1]
    if i == 0:
        print('Top 10 articles similar to: ' + term)
    else:
        print(f'{i:2d}. ' + term + ' : ' + str(rank[i][1]))


conn.close()
fr.close()
