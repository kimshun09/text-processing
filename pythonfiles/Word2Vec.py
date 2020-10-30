# coding: UTF-8

import os
from gensim.models import word2vec
import logging

wiki = 100
wkcfile = '../tmp/wakachi' + str(wiki) + '.txt'
modelfile = '../tmp/model' + str(wiki) + '.txt'

if os.path.exists(wkcfile) == False:
    print(wkcfile + ' doesn\'t exist')
    exit()
if os.path.exists(modelfile) == True:
    print(wkcfile + ' already exists.')
    yesno = input('continue? (yes/no): ')
    if yesno != 'yes':
        exit()


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = word2vec.Text8Corpus(wkcfile)
model = word2vec.Word2Vec(sentences, size=200, window=15)
model.save(modelfile)

