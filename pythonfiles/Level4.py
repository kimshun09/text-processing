# coding: UTF-8

import os
import sys
from gensim.models import word2vec

word = sys.argv[1]
wiki = 100
modelfile = '../tmp/model' + str(wiki) + '.txt'

if os.path.exists(modelfile) == False:
    print(modelfile + ' doesn\'t exist')
    exit()

model = word2vec.Word2Vec.load(modelfile)
results = model.wv.most_similar(positive=[word])
for result in results:
    print(result)