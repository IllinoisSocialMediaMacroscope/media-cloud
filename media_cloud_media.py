import requests
import os
import csv

class media:
    def __init__(self, API_key):
        self.key = API_key
        self.media_list = {}
        with open('media.csv','r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.media_list[row[0]] = row[2].replace(' ', '_')

    def get_single_media_info(self,media_id):
        params = { 'key': self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/media/single/' + str(media_id), 
                            params = params, 
                             headers = { 'Accept': 'application/json'} )
        response = r.json()
        if response != []:
            headers = ['is_healthy', 'is_monitored', 'media_id', 'name', 'public_notes', 'url']
            headers2 = ['description', 'label', 'show_on_media', 'show_on_stories', 'tag', 'tag_set', 'tag_sets_id', 'tags_id']

            # make directory
            name = self.media_list[str(media_id)]
            if not os.path.exists(name + '_info'):
                os.makedirs(name + '_info')
            with open(name + '_info/basics.csv','w',newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerow([response[0]['is_healthy'],
                                 response[0]['is_monitored'],
                                 response[0]['media_id'],
                                 response[0]['name'],
                                 response[0]['public_notes'],
                                 response[0]['url']])
            print('save results to ' + name + '_info/basics.csv')

            with open(name + '_info/media_source_tags.csv','w',newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers2)
                for t in response[0]['media_source_tags']:
                    writer.writerow([t['description'],
                                    t['label'],
                                    t['show_on_media'],
                                    t['show_on_stories'],
                                    t['tag'],
                                    t['tag_set'],
                                    t['tag_sets_id'],
                                    t['tags_id']])
            print('save results to ' + name + '_info/media_source_tags.csv')


    def get_media_health(self,media_id):
        params = { 'media_id':media_id, 'key': self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/mediahealth/list', 
                            params = params, 
                            headers = { 'Accept': 'application/json'} )
        response = r.json()
        if response != []:
            headers = ['coverage_gaps',
                       'end_date',
                       'expected_sentences',
                       'expected_stories',
                       'has_active_feed',
                       'is_healthy',
                       'media_health_id',
                       'media_id',
                       'num_sentences',
                       'num_sentences_90',
                       'num_sentences_w',
                       'num_sentences_y',
                       'num_stories',
                       'num_stories_90',
                       'num_stories_w',
                       'num_stories_y',
                       'start_date']
            headers2 = response[0]['coverage_gaps_list'][0].keys()

            # make directory
            name = self.media_list[str(media_id)]
            if not os.path.exists(name + '_health'):
                os.makedirs(name + '_health')
            with open(name + '_health/basics.csv','w',newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerow([response[0]['coverage_gaps'],
                                 response[0]['end_date'],
                                 response[0]['expected_sentences'],
                                 response[0]['expected_stories'],
                                 response[0]['has_active_feed'],
                                 response[0]['is_healthy'],
                                 response[0]['media_health_id'],
                                 response[0]['media_id'],
                                 response[0]['num_sentences'],
                                 response[0]['num_sentences_90'],
                                 response[0]['num_sentences_w'],
                                 response[0]['num_sentences_y'],
                                 response[0]['num_stories'],
                                 response[0]['num_stories_90'],
                                 response[0]['num_stories_w'],
                                 response[0]['num_stories_y'],
                                 response[0]['start_date']])

            print('save results to ' + name + '_health/basics.csv')

            with open(name + '_health/coverage_gaps_list.csv','w',newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers2)
                for t in response[0]['coverage_gaps_list']:
                    writer.writerow([t['expected_sentences'],
                                     t['expected_stories'],
                                     t['media_id'],
                                     t['num_sentences'],
                                     t['num_stories'],
                                     t['stat_week']])
            print('save results to ' + name + '_health/coverage_gaps_list.csv')
        
if __name__ =='__main__':
    
    mc = media('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
    mc.get_single_media_info(2)
    mc.get_media_health(2)

