import requests
import os
import csv
import json

'''
Media Cloud associates tags with media sources, stories, and
individual sentences. A tag consists of a short snippet of text,
a tags_id, and tag_sets_id. Each tag belongs to a single tag set.
The tag set provides a separate name space for a group of related tags.
Each tag has a unique name ('tag') within its tag set.
Each tag set consists of a tag_sets_id and a uniaue name.

For example, the 'gv_country' tag set includes the tags japan,
brazil, haiti and so on. Each of these tags is associated with
some number of media sources (indicating that the given media
source has been cited in a story tagged with the given country
in a Global Voices post).
'''

class tag:
    def __init__(self, API_key):
        self.key =API_key


    def get_single_tag(self, tag_id):
        params = { 'key': self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/tags/single/' + tag_id,
                         params = params,
                         headers = {'Accept':'application/json'} )
        response = r.json()
        with open('tag-' + tag_id + '.txt','w') as f:
            json.dump(response[0],f, indent=2)
        print('results are saved to tag-' + tag_id + '.txt')


        
    def get_tags_list(self, last_tags_id, tag_sets_id,rows, public, search, similar_tags_id):
        params = {'last_tags_id':last_tags_id,
                  'tag_sets_id':tag_sets_id,
                  'rows':rows,
                  'public':public,
                  'search':search,
                  'similar_tags_id':similar_tags_id,
                  'key':self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/tags/list/',
                         params = params,
                         headers = {'Accept':'application/json' } )
        response = r.json()
        with open('tags_list.csv','w',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['label','description','is_static','show_on_media','show_on_stories','tag',
                             'tag_set_description','tag_set_label','tag_set_name','tag_sets_id','tags_id'])
            for item in response:
                writer.writerow([item['label'],item['description'],
                                 item['is_static'], item['show_on_media'],
                                 item['show_on_stories'], item['tag'],
                                 item['tag_set_description'], item['tag_set_label'],
                                 item['tag_set_name'], item['tag_sets_id'], item['tags_id']])
        print('results are saved to tags_list.csv')

    def get_single_tag_sets(self,tag_sets_id):
        params = {'key':self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/tag_sets/single/' + tag_sets_id,
                         params = params,
                         headers = {'Accept': 'application/json' })
        response = r.json()
        with open('tagSets-' + tag_sets_id + '.txt','w') as f:
            json.dump(response[0],f, indent=2)
        print('results are saved to tagSets-' + tag_sets_id + '.txt')

    def get_tag_sets_list(self,last_tag_sets_id,rows):
        params = {'key':self.key, 'last_tag_sets_id':last_tag_sets_id, 'rows':rows}
        r = requests.get('https://api.mediacloud.org/api/v2/tag_sets/list/',
                         params = params,
                         headers = {'Accept': 'application/json' })
        response = r.json()
        with open('tag_sets_list.csv','w',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['label','description','name','show_on_media', 'show_on_stories','tag_sets_id'])
            for item in response:
                writer.writerow([item['label'], item['description'],
                                 item['name'],item['show_on_media'],
                                 item['show_on_stories'],
                                 item['tag_sets_id']])
        print('results are saved to tag_sets_list.csv')


                

if __name__ =='__main__':

    mc = tag('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
    mc.get_single_tag('8875027')
    mc.get_tags_list(last_tags_id=0, tag_sets_id=None, rows=100, public=1, search=None, similar_tags_id=None)
    mc.get_single_tag_sets('5')
    mc.get_tag_sets_list(0,100)
