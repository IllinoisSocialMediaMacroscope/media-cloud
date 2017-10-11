import requests
import os
import csv
import json

'''
Returns word frequency counts of the most common words
in a randomly sampled set of all sentences returned by
querying Solr using the q and fq parameters, with stopwords removed by default. Words are stemmed before being counted. For each word, the call returns the stem and the full term most used with the given stem in the specified Solr query (for example, in the below example, 'democrat' is the stem that appeared 58 times and
'democrats' is the word that was most commonly stemmed into 'democract').
'''

class word:
    def __init__(self, API_key):
        self.key =API_key


    def get_word_count_list(self, q, fq, num_words, sample_size):
        
        '''
        Parameter	    Default	Notes
        q	            n/a	        q ("query") parameter which is passed directly to Solr
        fq	            null	fq ("filter query") parameter which is passed directly to Solr
        num_words	    500	        Number of words to return
        sample_size	    1000	Number of sentences to sample, max 100,000
        include_stopwords   0	        Set to 1 to disable stopword removal
        include_stats	    0	        Set to 1 to include stats about the request as a whole (such as total number of words)
        '''
        params = {'q':q,
                  'fq':fq,
                  'num_words':num_words,
                  'sample_size': sample_size,
                  'include_stats':1,
                  'key':self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/wc/list',
                             params = params,
                             headers = {'Accept':'application/json'} )
        response = r.json()
        # print(response)
        with open('word_count_list.csv','w',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['count','stem','term'])
            for item in response['words']:
                writer.writerow([item['count'], item['stem'],item['term']])
        print('results are saved to word_count_list.csv','\n')
        print('num_words_returned: ', response['stats']['num_words_returned'])
        print('num_sentences_returned: ', response['stats']['num_sentences_returned'])
        print('num_sentences_found: ', response['stats']['num_sentences_found'])
        print('num_words_param: ', response['stats']['num_words_param'])
        print('sample_size_param: ', response['stats']['sample_size_param'])
            




if __name__ =='__main__':

    mc = word('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
    mc.get_word_count_list(q="sentence:renewable+AND+energy",fq="", num_words=1, sample_size=1)
