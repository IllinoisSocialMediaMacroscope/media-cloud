
![alt text](https://static1.squarespace.com/static/58cc2ac0cd0f68fdc8eb3753/t/58e518de9f7456846dd5a31f/1507310416358/?format=1500w)
# Media Cloud 
## An open-source platform for studying media ecosystems.
- website: https://mediacloud.org/
- api documentation: https://github.com/berkmancenter/mediacloud/blob/master/doc/api_2_0_spec/api_2_0_spec.md
- python sdk (no documentation though): https://github.com/mitmedialab/MediaCloud-API-Client

## Register on the website to use this script
- registration link: https://sources.mediacloud.org/#/user/signup
- After you have registered and activated, find your **API_Key** here: https://sources.mediacloud.org/#/user/profile

## Profile and Overview


```python
import media_cloud_profile as mc_profile

# subtitute with your own API key. This one is no longer valid!!
profile = mc_profile.profile(API_key = 'f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
```

#### profile


```python
profile.get_profile()
```

    role:  search
    created date:  2017-10-11T21:59:31
    email:  chenwang.carrie@gmail.com
    full name:  Chen Wang
    weekly requested items (limit/used):  100000/666
    weekly requested (limit/used):  10000/666
    notes:  Developer 
    

#### overall stats


```python
profile.get_stats_list()
```

    total stories:  546640512
    total_downloads:  961951872
    total sentences:  7247441920
    active_crawled_media:  46418
    active_cralwed_feeds:  94012
    daily_stories:  439897
    daily_downloads:  668157
    

## Media


```python
import media_cloud_media as mc_media

# subtitute with your own API key. This one is no longer valid!!
media = mc_media.media(API_key ='f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
```

#### get single media information


```python
media.get_single_media_info(media_id = 1)
```

    save results to New_York_Times_info/basics.csv
    save results to New_York_Times_info/media_source_tags.csv
    

#### get the health information of a media


```python
media.get_media_health(media_id = 1)
```

    save results to New_York_Times_health/basics.csv
    save results to New_York_Times_health/coverage_gaps_list.csv
    

## Feed


```python
import media_cloud_feeds as mc_feeds

# subtitute with your own API key. This one is no longer valid!!
feeds = mc_feeds.feed('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
```

#### get single feed informatioin


```python
feeds.get_single_feed(feed_id = 2)
```

    save results to DealBook_feed/basic.txt
    save results to DealBook_feed/rss.xml
    

#### get a list of feed information


```python
feeds.get_feed_list(total_num=100, media_id=2)
```

    done!
    save results to feed_list.csv
    

## Story 
- q is the query 
- fq is the psuedo query (filter)


```python
import media_cloud_stories as mc_stories

# subtitute with your own API key. This one is no longer valid!!
stories = mc_stories.story('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
```

#### get single story by ID


```python
stories.get_single_story(stories_id=27456565)
```

    save results to story-27456565.txt
    

#### get story list


```python
stories.get_story_list(last_processed_stories_id=0,rows=10, q='media_id:1', fq='')
```

    save results to 'story_list.csv'
    save results to 'feed_list_feeds.csv'
    save results to 'feed_list_wordCount.csv'
    save results to 'feed_list_storyTags.csv'
    

#### get story count


```python
stories.get_story_count(q="sentence:daca", fq="media_id:1")
```

    There are 252 stories that satisfy your query: sentence:daca and pseudo query: media_id:1
    

#### get the word matrix of the story


```python
stories.get_story_word_matrix(q="sentence:trump",fq="media_id:1",rows=10, max_words=100, stopword_length='tiny')
```

    save results to 'word_matrix.txt'
    

## Sentence


```python
import media_cloud_sentences as mc_sentences

# subtitute with your own API key. This one is no longer valid!!
sentences = mc_sentences.sentence('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
```

#### get sentence count based on query and filters


```python
sentences.get_sentence_count(q="sentence:renewable energy",
                              fq="",
                              split="1",
                              split_start_date="2017-01-01",
                              split_end_date="2017-07-01")
```

    There are 18098358 sentences that satisfy your query: sentence:renewable energy and pseudo query: 
    You have set the split to be true, a splitted count file will be saved to split_count.csv!
    

#### get sentence field count based on query and filters


```python
sentences.get_sentence_field_count(q="trump",fq="media_id:1", sample_size="100")
```

    num_sentences_found:  192582 
    num_sentences_returned:  100 
    sample_size_param:  100 
    
    results are saved to sentence_field_count.csv
    

## Word


```python
import media_cloud_word as mc_word

# subtitute with your own API key. This one is no longer valid!!
words = mc_word.word('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
```

#### get word count list based on query and filters


```python
words.get_word_count_list(q="sentence:renewable+AND+energy",fq="", num_words=1, sample_size=1)
```

    results are saved to word_count_list.csv 
    
    num_words_returned:  1 
     num_sentences_returned:  1 
     num_sentences_found:  1614748613 
     num_words_param:  1 
     sample_size_param:  1 
    
    

## Tag


```python
import media_cloud_tags as mc_tags

# subtitute with your own API key. This one is no longer valid!!
tags = mc_tags.tag('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
```

#### get single Tag by ID


```python
tags.get_single_tag('8875027')
```

    results are saved to tag-8875027.txt
    

#### get a list of tags


```python
tags.get_tags_list(last_tags_id=0, tag_sets_id=None, rows=100, public=1, search=None, similar_tags_id=None)
```

    results are saved to tags_list.csv
    

#### get single tag set by ID


```python
tags.get_single_tag_sets(tag_sets_id = '5')
```

    results are saved to tagSets-5.txt
    

### get a list of tag sets


```python
tags.get_tag_sets_list(last_tag_sets_id = 0, rows = 100)
```

    results are saved to tag_sets_list.csv
    

## Topic


```python
import media_cloud_topics as mc_topics

# subtitute with your own API key. This one is no longer valid!!
topics = mc_topics.topic('f317d30a4559267ce4a28bffb7a3020116326a27947573b88abe85f0bc0dd672')
```

#### get single topic by ID


```python
topics.get_single_topic(topic_id = '5')
```

    results are saved to topic-5.txt
    

#### get a list of topic by name


```python
topics.get_topics_list(name="Trump")
```

    results are saved to topics-list.txt
    
