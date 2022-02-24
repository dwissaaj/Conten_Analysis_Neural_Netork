import pandas as pd
import tweepy

Client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAK%2BeAwEAAAAAQSIOcQ2eSaCCfIYIpPrblFrH8cE%3DYrewCOd02CBazf5nrPlaA7cy0kMi9qzgJ8ThoN3cdpzy6Dq9BK")

textsrt = []
textgum = []
for tweet in tweepy.Paginator(Client.search_recent_tweets,query="indihome",max_results=100,
                              start_time = "2022-02-17T00:00:00Z",
                              end_time="2022-02-17T23:00:00Z",
                              tweet_fields=['created_at'],
                              user_fields=['username','profile_image_url'],
                              expansions=['author_id']).flatten(limit=5000):
   textsrt.append(tweet.text)

for tweet in tweepy.Paginator(Client.search_recent_tweets,query="indihome",max_results=100,
                              start_time = "2022-02-17T00:00:00Z",
                              end_time="2022-02-17T23:00:00Z",
                              tweet_fields=['created_at'],
                              user_fields=['username','profile_image_url'],
                              expansions=['author_id']).flatten(limit=800):
   textgum.append(tweet.text)


dfsrt = pd.DataFrame(textsrt)
dfgum = pd.DataFrame(textgum)
dfsrt.to_excel("17-02.xlsx")
dfgum.to_excel("gum 17-02.xlsx")












"""

response = Clien.search_recent_tweets(query="indihome",
                                  end_time="2022-02-15T23:00:00Z",
                                  start_time = "2022-02-15T00:00:00Z",
                                  max_results=10,tweet_fields=['created_at'],user_fields=['username','profile_image_url']
                                 ,expansions=['author_id'])

response = Clien.search_recent_tweets(query="indihome",
                                  end_time="2022-02-15T23:00:00Z",
                                  start_time = "2022-02-15T00:00:00Z",
                                  max_results=10,tweet_fields=['created_at'],user_fields=['username','profile_image_url']
                                 ,expansions=['author_id'])
#profile_image_url
users = {u['id']: u for u in response.includes['users']}
for tweet in response.data:
    user = users[tweet.author_id]
    text.append(tweet.text)
    data_items = users.items()
    data_list = list(data_items)
    df = pd.DataFrame(data_list)


df2 = pd.DataFrame(text)
df3 = pd.concat([df,df2],axis=1)
df3.to_excel("testing1.xlsx")"""

