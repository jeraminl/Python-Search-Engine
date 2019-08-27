'''
search.py

takes care of user input and queries the index for matching documents

'''

from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer as PS
from nltk.corpus import stopwords
import json
import math
import operator
import os
import traceback

class SearchEngine:
    def __init__(self, database, bookKeeperName):

        file = open(database, 'r')
        self.database = json.load(file)
        self.ps = PS()
        self.stopwords = set(stopwords.words('english'))
        self.corpusSize = 28249
        self.book = {}
        self.bookKeeperName = bookKeeperName

        #print(len(self.database))
        file = open(os.path.join('WEBPAGES_RAW', self.bookKeeperName))
        self.book = json.load(file)


    def search(self):
        #file = open(os.path.join('WEBPAGES_RAW', self.bookKeeperName))
        #self.book = json.load(file)
        while True:
            try:
                user_input = input("what would you like to search?").lower()
                queries = self.format_query(user_input)
                ranking = self.docRanking(queries)
                if len(ranking) > 0:
                    self.retrieveDoc(ranking)
                else:
                    print("no result for the given query")
            except Exception:
                 traceback.print_exc()

        #qtoken = query.split()
    def format_query(self, queries):
        tokens = RegexpTokenizer(r'\w+').tokenize(queries)
        stemmed = [self.ps.stem(t.lower()) for t in tokens]
        filtered = [t for t in stemmed if not t in self.stopwords]
        return filtered

    def docRanking(self, queries):
        ranking = {}
        for query in queries:
            try:
                for key in self.database[query].keys():
                    tf_idf = self.database[query][key]['tf-idf']
                    if key in ranking:
                        ranking[key] += tf_idf
                    else:
                        ranking[key] = tf_idf
            except KeyError:
                print('this word does not exist in the index')
        return dict(sorted(ranking.items(), key=lambda x: (-x[1], x[0]), reverse=False))


    def retrieveDoc(self, ranking):
        #print(ranking)
        result = {}
        i = 0
        print("total document found: " + str(len(ranking)))
        print("Top 20 result: ")
        for key in ranking.keys():
            if i < 20:
                print(str(i+1)+"\t" + key + "\t" + self.book[key])
                i+=1

'''
if __name__=='__main__':
    se = SearchEngine('index.json', 'bookkeeping.json')
    se.search()


for key in se.database.keys():
print(key)
print(len(se.database.keys()))
'''
