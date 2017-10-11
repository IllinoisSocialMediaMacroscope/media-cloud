import requests
import os

class profile:
    def __init__(self, API_key):
        self.key = API_key

    def get_profile(self):
        params = {'key': self.key}
        r = requests.get('https://api.mediacloud.org/api/v2/auth/profile',
                         params = params,
                         headers = {'Accept':'application/json'} )

        response = r.json()
        print('role: ', response['auth_roles'][0])
        print('created date: ', response['created_date'])
        print('email: ', response['email'])
        print('full name: ', response['full_name'])
        print('weekly requested items (limit/used): ', str(response['limits']['weekly']['requested_items']['limit']) + '/' +
              str(response['limits']['weekly']['requested_items']['used']))
        print('weekly requested (limit/used): ', str(response['limits']['weekly']['requests']['limit']) + '/' +
              str(response['limits']['weekly']['requests']['used']))
        print('notes: ', response['notes'])

    def get_stats_list(self):
        params = {'key':self.key}
        r = requests.get('https://api.mediacloud.org/api/v2/stats/list',
                         params = params,
                         headers = {'Accept':'application/json'} )
        response = r.json()
        print('total stories: ', response['total_stories'])
        print('total_downloads: ', response['total_downloads'])
        print('total sentences: ', response['total_sentences'])
        print('active_crawled_media: ', response['active_crawled_media'])
        print('active_cralwed_feeds: ', response['active_crawled_feeds'])
        print('daily_stories: ', response['daily_stories'])
        print('daily_downloads: ', response['daily_downloads'])
        

if __name__ == '__main__':

    mc = profile('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
    mc.get_profile()
    mc. get_stats_list()
