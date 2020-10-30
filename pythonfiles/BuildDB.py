# coding: UTF-8

import codecs
import os
import sys
import sqlite3

args = sys.argv # コマンドライン引数取得

path = args[1] # wikiのテキストファイルへのパス
filename = args[2] # wiki100またはwiki2700を指定

# データベースに接続
if os.path.exists('../database/' + filename + '.db'):
    os.remove('../database/' + filename + '.db')
conn = sqlite3.connect('../database/' + filename + '.db')
c = conn.cursor()

# テーブルarticlesの作成
# tag : タグ <doc ...>, entry : 見出し語, body : 本文
c.execute('CREATE TABLE articles(tag, entry, body)')

f = codecs.open(path + filename + '.txt', 'r', 'utf-8') # wikiのテキストファイルを開く

# 1行ずつ読み込む
line = f.readline()
while line:
    tag = line
    line = f.readline()
    entry = line
    line = f.readline()
    line = f.readline()
    body = ''
    while line!='</doc>\n' and line!='</doc>':
        body += line
        line = f.readline()
    sql = 'INSERT INTO articles (tag, entry, body) values (?, ?, ?)' # sql文
    article = (tag, entry, body) # 変数
    c.execute(sql, article) # sql文に変数を代入し実行
    line = f.readline()

conn.commit() # データベース保存
conn.close() # データベース切断
f.close() # ファイルを閉じる