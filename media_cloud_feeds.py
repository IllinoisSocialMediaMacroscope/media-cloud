import requests
import os
import csv
import json

class feed:
    def __init__(self, API_key):
        self.key = API_key

    def get_single_feed(self,feed_id):
        params = {'key':self.key }
        r = requests.get('https://api.mediacloud.org/api/v2/feeds/single/' + str(feed_id),
                         params = params,
                         headers = {'Accept':'application/json'} )
        response = r.json()
        if response != []:
             # make directory
            name = response[0]['name'].replace(" ","_")
            if not os.path.exists(name + '_feed'):
                os.makedirs(name + '_feed')
                
            with open( name +'_feed/basic.txt', 'w') as outfile:
                json.dump(response[0], outfile)

            # download the rss
            r2 = requests.get(response[0]['url'])
            with open( name +'_feed/rss.xml', 'w') as f:
                f.write(r2.content.decode("utf-8") )

    def get_feed_list(self, total_num, media_id):
        last_id = 0
        count = 0
        feeds = []
        
        while True:
            count += 1
            params = {'last_feeds_id':last_id,  'rows':100, 'media_id':media_id,'key':self.key }
            r = requests.get('https://api.mediacloud.org/api/v2/feeds/list',
                             params = params,
                             headers = {'Accept':'application/json'} )
            response = r.json()
            feeds.extend(response)
            
            if  response == []:
                print('reach the bottom of the available feeds!')
                break
            if count * 100 >= total_num:
                print('done!')
                break

        if feeds != []:
            with open('feed_list.csv', 'w',newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(['name','url','feeds_id','feed_type','media_id'])
                for item in feeds:
                    writer.writerow([item['name'],
                                     item['url'],
                                     item['feeds_id'],
                                     item['feed_type'],
                                     item['media_id']])        
    


if __name__ =='__main__':
    
    mc = feed('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
    mc.get_single_feed(2)
    mc.get_feed_list(total_num=100, media_id=2)
