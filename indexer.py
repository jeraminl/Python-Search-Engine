'''
    indexer.py
    given an html file, calls Tokenizer to tokenize the content and add it to a database
    index:
        token:
            key (doc id):
                tf (term frequency): 0
                tf-idf: 0
'''
import traceback
import os.path
import tokenizer
import json
import re
import math
from urllib.parse import urlparse

class Indexer:
    def __init__(self, fileName):
        self.bookKeeperName = fileName
        self.book = {}
        self.index = {}
        self.tk = tokenizer.Tokenizer()
        self.total = 0
        self.indexSize = 0


    def runIndexer(self):
        file = open(os.path.join('WEBPAGES_RAW', self.bookKeeperName))
        self.book = json.load(file)
        self.iterateBook()
        self.calculate_TF_IDF()
        self.addToDatabase()


    def iterateBook(self):
        i = 0
        for key in self.book:
            #print(key)
            i += 1
            if self.is_valid(self.book[key]):
                #print('passed')
                self.total+=1
                self.addTokens(key)
                print('total file parsed: ' + str(self.total) + "   "+ str(round((i/37497)*100,2))+'%')

        print(len(self.index))

    def addTokens(self, key):
        try:

            #print(len(self.index))
            file = open(os.path.join('WEBPAGES_RAW',key),'rb')
            title, heading, body = self.tk.parseHTML(file.read())
            if title != None:
                i = 0
                for token in title:
                    if token not in self.index.keys():
                        # token ->  {docID: (freq, TF-IDF)} note: TF-IDF set to 0 at first indexing, has to go through again to calculate
                        self.index[token] = {key: {'tf':5 ,'pos': [i]}}

                    else:
                        if key not in self.index[token].keys():
                            self.index[token][key] = {'tf':5, 'pos': [i]}

                        else:
                            self.index[token][key]['tf'] += 5
                            self.index[token][key]['pos'].append(i)
                i += 1

            if heading != None:
                i = 0
                for token in heading:
                    if token not in self.index.keys():
                        # token ->  {docID: (freq, TF-IDF)} note: TF-IDF set to 0 at first indexing, has to go through again to calculate
                        self.index[token] = {key: {'tf':3 ,'pos': [i]}}

                    else:
                        if key not in self.index[token].keys():
                            self.index[token][key] = {'tf':3, 'pos': [i]}

                        else:
                            self.index[token][key]['tf'] += 3
                            self.index[token][key]['pos'].append(i)
                i += 1

            if body != None:
                i = 0

                for token in body:
                    if token not in self.index.keys():
                        # token ->  {docID: (freq, TF-IDF)} note: TF-IDF set to 0 at first indexing, has to go through again to calculate
                        self.index[token] = {key: {'tf':1 ,'pos': [i]}}

                    else:
                        if key not in self.index[token].keys():
                            self.index[token][key] = {'tf':1, 'pos': [i]}

                        else:
                            self.index[token][key]['tf'] += 1
                            self.index[token][key]['pos'].append(i)
                i += 1
            file.close()
            self.indexSize = len(self.index.keys())
        except Exception:
             traceback.print_exc()

    def calculate_TF_IDF(self):
        i = 0
        for token in self.index.keys():
            print("calculating TF-IDF: " + str(round(i/len(self.index) * 100,2))+'%') # for tracking indexing progress by 5
            i += 1
            for key in self.index[token].keys():
                tf = (1 + math.log10(self.index[token][key]['tf']))
                idf = math.log10(self.total/len(self.index[token]))
                tf_idf = tf*idf
                self.index[token][key] = {'tf-idf': round(tf_idf,2)}

    def addToDatabase(self):
        with open('index.json', 'w') as json_file:
            json.dump(self.index, json_file, separators = (',', ':'), indent=0)


    def is_valid(self, url):
            """
            Function returns True or False based on whether the url has to be fetched or not. This is a great place to
            filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
            in this method
            """
            pattern = re.compile(r"=([0-9a-fA-F]{32,})$")
            parsed = urlparse('https://'+ url)
            if parsed.scheme not in set(["http", "https"]):
                return False
            #if url is too long
            if (len(url) > 150):
                return False

            '''
                conditions for traps
                1. what the professor gave us
                2. checking for repeating subdirectories
                3. checking for long hex sequences
            '''
            try:
                if ".ics.uci.edu" in parsed.hostname \
                       and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                        + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                        + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                        + "|thmx|mso|arff|rtf|jar|csv" \
                                        + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower()) \
                                        and not re.search(r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", parsed.path.lower()) \
                                        and not re.search(pattern, parsed.query.lower()):
                    return True
                else:
                    return False

                                        #and not re.match("^.*calendar.*$", parsed.path.lower())  \


            except TypeError:
                print("TypeError for ", parsed)
            return False

if __name__ == '__main__':
    i = Indexer('bookkeeping.json')
    i.runIndexer()
