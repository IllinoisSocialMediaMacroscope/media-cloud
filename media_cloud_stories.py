import requests
import os
import csv
import json

'''
A story represents a single published piece of content. Each unique URL
downloaded from any syndicated feed within a single media source
is represented by a single story. For example, a single New York
Times newspaper story is a Media Cloud story, as is a single
Instapundit blog post. Only one story may exist for a given title
for each 24 hours within a single media source.'''

class story:
    def __init__(self, API_key):
        self.key = API_key


    def get_single_story(self, stories_id):
        params = {'key':self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/stories_public/single/' + str(stories_id),
                             params = params,
                             headers = {'Accept':'application/json'} )
        response = r.json()
        if response != []:
            with open( 'story-'+ str(response[0]['stories_id'])+ '.txt', 'w') as outfile:
                json.dump(response[0], outfile,indent=2)
            print('save results to story-' + str(response[0]['stories_id'])+ '.txt')
                  

    def get_story_list(self, last_processed_stories_id, rows, q, fq, wc=1, show_feeds=1):
        params = {'last_processed_stories_id': last_processed_stories_id, 
                  'rows': rows,
                  'q':q,
                  'fq':fq,
                  'wc':wc,
                  'show_feeds':show_feeds,
                  'key':self.key}
        
        r = requests.get( 'https://api.mediacloud.org/api/v2/stories_public/list/',
                           params = params,
                           headers = { 'Accept': 'application/json'} )
        response = r.json()
        if response != []:
            feeds_field = []
            word_count = []
            story_tags = []
            
            with open('story_list.csv','w',newline="") as f:
                writer = csv.writer(f)
                writer.writerow(['ap_syndicated',
                                  'bitly_click_count',
                                  'collect_date',
                                  'guid',
                                  'language',
                                  'media_id',
                                  'media_name',
                                  'media_url',
                                  'processed_stories_id',
                                  'publish_date',
                                  'stories_id',
                                  'title',
                                  'url'])

                for item in response:
                    writer.writerow([item['ap_syndicated'],
                                      item['bitly_click_count'],
                                      item['collect_date'],
                                      item['guid'],
                                      item['language'],
                                      item['media_id'],
                                      item['media_name'],
                                      item['media_url'],
                                      item['processed_stories_id'],
                                      item['publish_date'],
                                      item['stories_id'],
                                      item['title'],
                                      item['url']])
                    for i in item['feeds']:
                        feeds_field.append([item['stories_id'],i['feed_type'],i['feeds_id'],i['media_id'],i['url']])
                    for i in item['word_count']:
                        word_count.append([item['stories_id'],i['count'],i['stem'],i['term']])
                    for i in item['story_tags']:
                        story_tags.append([item['stories_id'],i['tag'],
                                          i['tag_set'],i['tag_sets_id'],i['tags_id']])
            print('save results to \'story_list.csv\'')
            
            with open('feed_list_feeds.csv', 'w',newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(['stories_id','feed_type','feeds_id','media_id','url'])
                writer.writerows(feeds_field)
            print('save results to \'feed_list_feeds.csv\'')
                                          
            with open('feed_list_wordCount.csv', 'w',newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(['stories_id','count','stem','term'])
                writer.writerows(word_count)
            print('save results to \'feed_list_wordCount.csv\'')
            
            with open('feed_list_storyTags.csv', 'w',newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(['stories_id','tag','tag_set','tag_sets_id','tags_id'])
                writer.writerows(story_tags)           
            print('save results to \'feed_list_storyTags.csv\'')
            
            ''' q parameter
            Field	            Description
            sentence	            the text of the sentence
            stories_id	            a story ID
            media_id	            the Media Cloud media source ID of a story
            publish_date	    the publish date of a story
            tags_id_story	    the ID of a tag associated with a story
            tags_id_media	    the ID of a tag associated with a media source
            processed_stories_id    the processed_stories_id as returned by stories_public/list
            '''

            ''' fq parameter
            Pseudo Query Field	Description
            topic	        a topic id
            timespan	        a timespan id
            link_from_tag	a tag id, returns stories linked from stories associated with the tag
            link_to_story	a story id, returns stories that link to the story
            link_from_story	a story id, returns stories that are linked from the story
            link_to_medium	a medium id, returns stories that link to stories within the medium
            link_from_medium	link_from_medium, returns stories that are linked from stories within the medium
            '''

    def get_story_count(self,q,fq):
        params = {'q':q, 'fq':fq, 'key':self.key}
        r = requests.get( 'https://api.mediacloud.org/api/v2/stories_public/count',
                           params = params,
                           headers = { 'Accept': 'application/json'} )
        response = r.json()
        print("There are " + str(response['count']) + " stories that satisfy your query: " + q + " and pseudo query: " + fq)



    def get_story_word_matrix(self,q, fq,rows, max_words,stopword_length):
        params = {'q':q,
                  'fq':fq,
                  'rows':rows,
                  'max_words':max_words,
                  'stopword_length':stopword_length,
                  'key':self.key }
        r = requests.get( 'https://api.mediacloud.org/api/v2/stories_public/word_matrix',
                           params = params,
                           headers = { 'Accept': 'application/json'} )
        response = r.json()
        with open( 'word_matrix.txt', 'w') as outfile:
            json.dump(response, outfile,indent=2)
        print('save results to \'word_matrix.txt\'')

        '''
        Parameter	Default	Notes
        q	        n/a	q ("query") parameter which is passed directly to Solr
        fq	        null	fq ("filter query") parameter which is passed directly to Solr
        rows	        1000	number of stories to return from solr, max 100,000
        max_words	n/a	max number of non-zero count word stems to return for each story
        stopword_length	n/a	if set to 'tiny', 'short', or 'long', eliminate stop word list of that length
        '''

    

        
if __name__ =='__main__':
    
    mc = story('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
    mc.get_single_story(27456565)
    mc.get_story_list(0, 10, 'media_id:1', '')
    mc.get_story_count("sentence:daca","media_id:1")
    mc.get_story_word_matrix(q="sentence:trump",fq="media_id:1",rows=10, max_words=100, stopword_length='tiny')
