import requests
import os
import csv
import json

'''
Topics are collections of stories within some date range
that match some pattern indicating that they belong to some topic.
Topics both stories matched from crawled Media Cloud content and
stories discovered by spidering out from the links of those matched
stories. For more information about topics and how they are generated, see:

http://cyber.law.harvard.edu/publications/2013/social_mobilization_and_the_networked_public_sphere

A single topic is the umbrella object that represents the whole topic.
A snapshot is a frozen version of the data within a topic that
keeps a consistent view of a topic for researchers and also includes
analytical results like link counts. A timespan represents the set
of stories active in a topic within a given date range. Every timespan
belongs to a snapshot.

Topic data can be used to search stories and media sources as well.
Use the timespans_id param to list the media sources within a given
timespan. See the documentation for Solr pseudo queries for documentation
of how to query for stories within a topic.
'''

class topic:
    def __init__(self, API_key):
        self.key =API_key

    def get_single_topic(self,topic_id):
        params = { 'key': self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/topics/single/' + topic_id,
                         params = params,
                         headers = {'Accept':'application/json'})
        response = r.json()
        # print(response)
        with open('topic-' + topic_id + '.txt','w') as f:
            json.dump(response['topics'],f, indent=2)
        print('results are saved to topic-' + topic_id + '.txt')

    def get_topics_list(self, name):
        params = {'name':name, 'key':self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/topics/list',
                         params = params,
                         headers = {'Accept': 'application/json'} )
        response = r.json()
        with open('topics-list.txt','w') as f:
            json.dump(response,f, indent=2)
        print('results are saved to topics-list.txt')

if __name__ =='__main__':

    mc = topic('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
    mc.get_single_topic('5')
    mc.get_topics_list(name="obama")
   
     

        
