import pandas as pd
import tweepy

Client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAK%2BeAwEAAAAAQSIOcQ2eSaCCfIYIpPrblFrH8cE%3DYrewCOd02CBazf5nrPlaA7cy0kMi9qzgJ8ThoN3cdpzy6Dq9BK")

textsrt = []
textgum = []
for tweet in tweepy.Paginator(Client.search_recent_tweets,query="telkomsel",max_results=100,
                              start_time = "2022-03-18T00:00:00Z",
                              end_time="2022-03-24T23:00:00Z",
                              tweet_fields=['created_at','lang : id'],
                              user_fields=['username'],
                              expansions=['author_id']).flatten(limit=100):
   textsrt.append(tweet.text)

dfsrt = pd.DataFrame(textsrt)











