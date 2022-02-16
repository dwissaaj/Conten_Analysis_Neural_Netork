import re
import nltk
import spacy
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
nlp = spacy.load('xx_ent_wiki_sm')
nlp.add_pipe('sentencizer')

stop = stopwords.words('indonesian')
"""
Load_data fun reading excel file and change to ascii encoding for
removing the emoji in dataframe
"""


def load_data(file):
    data = pd.read_excel(file)
    data = data.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
    return data

"""
Removing username in dataframe.You should this before use cleaning_data function
"""
def remove_username(dataframe,column:str):
    final = []
    for text in dataframe[column].values.astype(str):
        text = re.sub('@[\w]+','',text)
        final.append(text)
        df = pd.DataFrame(final,columns=[column])
    return df

"""
Removing all character,symbol and etc in dataframe
"""
def cleaning_data(dataframe,column:str):
    text = dataframe[column].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ',regex=True)
    text = text.str.replace(r"[\"\'\|\?\=\.\\#\*\+\!\:\,]", '',regex=True)
    text = text.str.replace('\d+', '',regex=True)
    text = text.str.replace('RT', '',regex=True)
    text = text.str.replace(r'\n',' ', regex=True)
    text = text.str.replace("\s\s+" , " ",regex=True)
    text = text.str.lstrip()

    return text.to_frame(name=column)

"""
Removing stopwords inside dataframe. Need install NLTK Stopwords to specify stopword list
"""

def remove_stopwords(dataframe,column:str,stop:str):
    from nltk.corpus import stopwords
    stop = stopwords.words('indonesian')
    data = dataframe[column].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    return data.to_frame(name=column)
"""
Tokenize using NLTK for split each word
"""
def generate_word(dataframe,column:str):
    data = dataframe[column].apply(word_tokenize)
    return data


df = load_data("data.xlsx")
df2 = remove_username(df,"text")
df3 = cleaning_data(df2,"text")
df4 = remove_stopwords(df3,"text","indonesian")
df5 = generate_word(df4,"text")


#CHECK AGAIN FOR SPARK NLP FOR LEMMATIZATION
"""
sentences = list(doc.sents)
data = spark.createDataFrame([["Peter Pipers employees are picking pecks of pickled peppers."]]) \
    .toDF("text")
lemmatizer = Lemmatizer().setInputCols(["token"]).setOutputCol("lemma")
pipeline = Pipeline().setStages([lemmatizer])
result = Pipeline.fit(data).transform(data)
result.selectExpr("lemma.result").show(truncate=False)
print(result)"""

"""

"""