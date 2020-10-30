# coding: UTF-8

import os
import time
import sys
import sqlite3

args = sys.argv # コマンドライン引数取得

filename = args[1] # wiki100またはwiki2700を指定
word = args[2] # 検索語

# データベースに接続
if os.path.exists('../database/' + filename + '.db') == False:
    print('../database/' + filename + '.db' + 'doesn\'t exist')
conn = sqlite3.connect('../database/' + filename + '.db')
c = conn.cursor()

regex = ('%' + word + '%',) # 検索語を一部に含む語の正規表現

start = time.time() # 開始時間
entries = c.execute('SELECT entry FROM articles WHERE entry LIKE ?', regex) # 検索結果をタプルで取得
end = time.time() # 終了時間

# 結果の表示
for entry in entries:
    print(entry[0])
print('retrieval time : ' + str(end-start) + 'sec') # 検索時間の表示


conn.commit() # データベース保存
conn.close() # データベース切断
