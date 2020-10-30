# coding: UTF-8

# 検索語とユーザプロファイルをもとに最も類似した記事トップ10を表示する

import codecs
import os
import sqlite3
import math

class Level3:

    def __init__(self, tfidffile):
        self.tfidf = self.get_tfidf(tfidffile)

    def get_tfidf(self, tfidffile):
        fr = codecs.open(tfidffile, 'r', 'utf-8')
        lines = fr.read().split('\n')[:-1]
        tfidf = []
        for line in lines:
            dic = {}
            if line == ' ':
                tfidf.append({' ': 0})
                continue
            terms = line.split(',')
            for term in terms:
                parts = term.split(':')
                dic[parts[0]] = float(parts[1])
            tfidf.append(dic)
        fr.close()
        return tfidf

    def get_id(self, word, c):
        regex = (word + '\n',)
        rowid = c.execute('select ROWID from ARTICLES where ENTRY like ?', regex)
        fetch = rowid.fetchone()
        if fetch == None:
            regex = (keyword + '%',)
            rowid = c.execute('select ROWID from ARTICLES where ENTRY like ?', regex)
            fetch = rowid.fetchone()
            if fetch == None:
                return -1
        id = fetch[0] - 1
        return id

    def get_usr_vec(self, profile, tfidf):
        usr_vec = {}
        line = ''
        words = profile.split(',')
        for word in words:
            word_id = self.get_id(word, c)
            if word_id == -1 or tfidf[word_id] == {' ', 0}:
                continue
            # ユーザプロファイルの単語それぞれに一致する記事のベクトルの和をとる
            usr_vec = self.vec_sum(usr_vec, tfidf[word_id])
            # ベクトルの平均をとったものがユーザベクトル
            usr_vec = self.vec_times(usr_vec, 1/len(words))
            line += self.get_entry(word_id, c) + ','
        print('Your favorites: ' + line[:-1])
        return usr_vec

    def get_entry(self, id, c):
        rowid = (id + 1,)
        entry = c.execute('select ENTRY from ARTICLES where ROWID = ?', rowid)
        term = entry.fetchone()[0][:-1]
        return term

    def vec_sum(self, a, b):
        vec = a
        for key in b:
            if key in vec.keys():
                vec[key] += b[key]
            else:
                vec[key] = b[key]
        return vec

    def vec_times(self, a, t):
        vec = a
        for key in a:
            vec[key] = t * vec[key]
        return vec

    def get_sml(self, vec, tfidf, c):
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
            sml[(i, self.get_entry(i, c))] = value
        return sml

    def get_rank(self, keyword, profile, c):
        key_id = self.get_id(keyword, c)
        if key_id == -1:
            print('no articles found')
            exit()
        key_vec = self.tfidf[key_id]
        if key_vec == {' ', 0}:
            print('try again')
            exit()
        usr_vec = self.get_usr_vec(profile, self.tfidf)
        # ユーザベクトルと索引後ベクトルの平均のベクトルをもとに類似度を求める
        vec = self.vec_sum(key_vec, usr_vec)
        vec = self.vec_times(vec, 1/2)
        sml = self.get_sml(vec, self.tfidf, c)
        # 類似度の高い順に並び替え
        rank = sorted(sml.items(), key=lambda x: x[1], reverse=True)
        return rank

    def get_body(self, id, c):
        rowid = (id + 1,)
        entry = c.execute('select BODY from ARTICLES where ROWID = ?', rowid)
        body = entry.fetchone()[0][:-1]
        return body


if __name__ == '__main__':

    keyword = input('Search word: ')
    profile = input('User profile(split with ,): ')

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

    lv3 = Level3(tfidffile)
    rank = lv3.get_rank(keyword, profile, c)

    while True:
        print('Top 10 articles similar to: ' + rank[0][0][1])
        for i in range(1, 11):
            print(f'{i:2d}. {rank[i][0][1]} : {rank[i][1]:.4f}')
        id = int(input('Select 1-10 (exit:0): '))
        if id == 0:
            break
        else:
            print(rank[id][0][1])
            print(lv3.get_body(rank[id][0][0], c))


    conn.close()
