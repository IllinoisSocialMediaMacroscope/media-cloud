import requests
import os
import csv
import json

'''
The text of every story processed by Media Cloud is parsed into
individual sentences. Duplicate sentences within the same media
source in the same week are dropped (the large majority of those
duplicate sentences are navigational snippets wrongly included in
the extracted text by the extractor algorithm).'''


class sentence:
    def __init__(self, API_key):
        self.key =API_key

    
    def get_sentence_count(self, q, fq, split, split_start_date, split_end_date):

        '''
        Parameter	    Default	Notes
        q	            n/a	        q ("query") parameter which is passed directly to Solr
        fq	            null	fq ("filter query") parameter which is passed directly to Solr
        split	            null	if set to 1 or true, split the counts into date ranges
        split_start_date    null	date on which to start date splits, in YYYY-MM-DD format
        split_end_date	    null	date on which to end date splits, in YYYY-MM-DD format
        '''

        params = {'q':q,
                  'fq':fq,
                  'split':split,
                  'split_start_date': split_start_date,
                  'split_end_date': split_end_date,
                  'key':self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/sentences/count',
                             params = params,
                             headers = {'Accept':'application/json'} )
        response = r.json()
        print("There are " + str(response['count']) + " sentences that satisfy your query: " + q + " and pseudo query: " + fq)
        if split == "1":
            with open('split_count.csv', 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(['date_range','count'])
                for key,value in response['split'].items():
                    if key != 'gap' and key !='end' and key!='start':
                        writer.writerow([key,value])
            print("You have set the split to be true, a splitted count file will be saved to split_count.csv!")



    def get_sentence_field_count(self, q, fq, sample_size):

        '''
        Parameter	Default	        Notes
        q	        n/a	        q ("query") parameter which is passed directly to Solr
        fq	        null	        fq ("filter query") parameter which is passed directly to Solr
        sample_size	1000	        number of sentences to sample, max 100,000
        include_stats	0	        include stats about the request as a whole
        field	        tags_id_stories	field to count
        tag_sets_id	null	        return only tags belonging to the given tag set
        '''

        params = {'q':q,
                  'fq':fq,
                  'sample_size':sample_size,
                  'include_stats': 1,
                  'key': self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/sentences/field_count',
                             params = params,
                             headers = {'Accept':'application/json'} )
        response = r.json()
        # print(response)

        with open('sentence_field_count.csv','w',newline="") as f:
            writer = csv.writer(f)
            header = ['count','tag_sets_id','label','tag','tags_id']
            writer.writerow(header)
            for item in response['counts']:
                try:
                    writer.writerow([item['count'],item['tag_sets_id'],item['label'],item['tag'],item['tags_id']])
                except:
                    pass
            print("num_sentences_found: ", response['stats']['num_sentences_found'], '\n'
                "num_sentences_returned: ", response['stats']['num_sentences_returned'], '\n'
                 "sample_size_param: ", response['stats']['sample_size_param'], '\n')
    
        print('results are saved to sentence_field_count.csv')

if __name__ =='__main__':

    mc = sentence('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
    mc.get_sentence_count(q="sentence:renewable energy",
                          fq="",
                          split="1",
                          split_start_date="2017-01-01",
                          split_end_date="2017-07-01")
    mc.get_sentence_field_count(q="trump",fq="media_id:1", sample_size="100")

    

    
