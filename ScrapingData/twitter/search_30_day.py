
import json

import pandas as pd
import tweepy
import pandas as pd
auth = tweepy.OAuth1UserHandler(
   "laQY4h8wZ6swfCBh2aiNHtawI", "VzaRu7TRp4J3k0Dy6TiXuOzLX8FO3XyUy8IYiXUGKlh6BMAJYr",
   "2209890762-3OUYElYDtZ7DZsqbmH8il6V7QPJPV40LB6y0mwb", "528FEgzYTpuIL0epN5KKy9Fn34hvUVfZP00F0pUILTKHn"
)
api = tweepy.API(auth)

tweet_get = api.search_tweets(q="indihome",count=1000,until="2022-02-14",result_type="recent")

created_at = []
id = []
id_str = []
text = []
truncated = []
entities = []
metadata = []
source = []
in_reply_to_status_id = []
in_reply_to_status_id_str = []
in_reply_to_user_id=[]
in_reply_to_user_id_str=[]
in_reply_to_screen_name=[]
user=[]
geo=[]
coordinates=[]
place=[]
contributors=[]
is_quote_status=[]
retweet_count=[]
favorite_count=[]
favorited=[]
retweeted=[]
possibly_sensitive=[]
lang=[]

for tweets in tweet_get:
    data = tweets._json
    created_at.append(data.get('created_at'))
    id.append(data.get('id'))
    id_str.append(data.get('id_str'))
    text.append(data.get('text'))
    truncated.append(data.get('truncated'))
    entities.append(data.get('entities'))
    source.append(data.get('source'))
    metadata.append(data.get('metadata'))
    in_reply_to_status_id.append(data.get('in_reply_to_status_id'))
    in_reply_to_status_id_str.append(data.get('in_reply_to_status_id_str'))
    in_reply_to_screen_name.append(data.get('in_reply_to_screen_name'))
    user.append(data.get('user'))
    geo.append(data.get('geo'))
    coordinates.append(data.get('coordinates'))
    place.append(data.get('place'))
    contributors.append(data.get('contributors'))
    is_quote_status.append(data.get('is_quote_status'))
    retweet_count.append(data.get('retweet_count'))
    favorite_count.append(data.get('favorite_count'))
    favorited.append(data.get('favorited'))
    retweeted.append(data.get('retweeted'))
    possibly_sensitive.append(data.get('possibly_sensitive'))
    lang.append(data.get('lang'))



df = pd.DataFrame({'created_at':created_at,
                   'id':id,
                   'id_str':id_str,
                   'text':text,
                   'truncated':truncated,
                   'entities':entities,
                   'source':source,
                   'metadata':metadata,
                   'in_reply_to_status_id':in_reply_to_status_id,
                   'in_reply_to_status_id_str':in_reply_to_status_id_str,
                   'in_reply_to_screen_name':in_reply_to_screen_name,
                   'user':user,
                   'geo':geo,
                   'coordinates':coordinates,
                   'place':place,
                   'contributors':contributors,
                   'is_quote_status':is_quote_status,
                   'retweet_count':retweet_count,
                   'favorite_count':favorite_count,
                   'favorited':favorited,
                   'retweeted':retweeted,
                   'possibly_sensitive':possibly_sensitive,
                   'lang':lang})

print("Named file \n")
naming = str(input())
df.to_excel(f"..\data_30_days\{naming}.xlsx")