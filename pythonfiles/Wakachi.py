# coding: UTF-8

import MeCab
import sqlite3
import os
import codecs


wiki = 100
dbfile = '../database/wiki' + str(wiki) + '.db'
wkcfile = '../tmp/wakachi' + str(wiki) + '.txt'

m = MeCab.Tagger('-Owakati')

if os.path.exists(dbfile) == False:
    print(dbfile + ' doesn\'t exist')
    exit()
if os.path.exists(wkcfile) == True:
    print(wkcfile + ' already exists.')
    yesno = input('continue? (yes/no): ')
    if yesno != 'yes':
        exit()

conn = sqlite3.connect(dbfile)
c = conn.cursor()
bodies = c.execute('select BODY from ARTICLES')

f = codecs.open(wkcfile, 'w', 'utf-8')

for i, body in enumerate(bodies):
    text = m.parse(body[0])
    f.write(text)
    print(i)

conn.close()
f.close()
