import re
import gensim.utils
import nltk
import spacy
import glob
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
nlp = spacy.load('xx_ent_wiki_sm')
nlp.add_pipe('sentencizer')
stopwords = stopwords.words("indonesian")

def load_data(file):
    data = pd.read_excel(file)
    data = data.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
    return data

def clean_data(df,column):
    text = df[column].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ',regex=True)
    text = text.str.replace(r"[\"\'\|\?\=\.\@\#\*\+\!\:\,]", '',regex=True)
    text = text.str.replace('\d+', '',regex=True)
    text = text.str.replace('RT', '',regex=True)
    text = text.str.replace(r'\n',' ', regex=True)
    text = text.str.replace("\s\s+" , " ",regex=True)
    text = text.str.lstrip()
    return text.to_frame(name=column)

def gen_words(texts):
    final = []
    for text in texts.iteritems():
        for word in enumerate(text):
            final.append(word)
    return final


df = load_data("data.xlsx")
clean = clean_data(df,"text")
doc = nlp(str(clean))
sentences = list(doc.sents)

docx = nlp("study studying belajar pelajari memakan makanan")
for word in docx:
    print(word.text + word.lemma_ + word.pos_)


"""def lemmatization(text):
    data = text().apply(lambda row: " ".join([w.lemma_ for w in model(row)]))
    return data"""
