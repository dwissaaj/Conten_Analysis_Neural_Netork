import newspaper
import numpy as np
import pandas as pd
from serpapi import GoogleSearch
from newspaper import Article


def scraping_link(query:str,start_day:str,start_month:str,start_year:str,end_day:str,end_month:str,end_year:str):
    params = {
        "tbm": "nws",
        "q": f"{query}",
        "location": "Jakarta",
        "hl": "id",
        "num": 20,
        "tbs": f"cdr:1,cd_min:{start_day}/{start_month}/{start_year},cd_max:{end_day}/{end_month}/{end_year}",
        "api_key": "03d39295ce583d1f73700a62f5fd56b76078215f63c82360e6d9d0cb34ff8f62"}
    search = GoogleSearch(params)
    result = search.get_dict()
    data = pd.DataFrame(result['news_results'])
    urls = data['link'].to_list()
    return urls

link = scraping_link("MNC Play","01","01","2018","08","03","2022")

data = []
for url in link:
    try:
        a = Article(url, language='id')
        a.download()
        a.parse()

    except newspaper.ArticleException as e:
        print(e)

    else:
        author = a.authors
        dates = a.publish_date
        add_data = a.additional_data
        text = a.text
        tag = a.tags
        title = a.title
        keywords = a.keywords


        new_df = pd.DataFrame({'penulis':[author],'tanggal':[dates],'additional':[add_data],'berita':[text],'tags':[tag],'judul':[title],'kata':[keywords]})
        data.append(new_df)

df = pd.concat(data)

df = df.replace(to_replace='None', value=np.nan).dropna()
old_dates = df['tanggal']
df['tanggal'] = df['tanggal'].apply(lambda a: pd.to_datetime(a).date())
df.to_excel("mnc.xlsx")