import re
import gensim
import spacy
import pyLDAvis
import warnings
import pandas as pd
import gensim.models.ldamodel
from gensim import corpora
from pyLDAvis import gensim_models
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

warnings.filterwarnings("ignore", category=DeprecationWarning)

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


def remove_username(dataframe, column: str):
    final = []
    for text in dataframe[column].values.astype(str):
        text = re.sub(r'@[\w]+', '', text)
        final.append(text)
        data = pd.DataFrame(final, columns=[column])
    return data


"""
Removing all character,symbol and etc in dataframe
"""


def cleaning_data(dataframe, column: str):
    text = dataframe[column].str.replace(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', regex=True)
    text = text.str.replace(r"[\"\'\|\?\=\.\\#\*\+\!\:\,]", '', regex=True)
    text = text.str.replace(r'\d+', '', regex=True)
    text = text.str.replace(r'RT', '', regex=True)
    text = text.str.replace(r'\n', ' ', regex=True)
    text = text.str.replace(r'\s\s+', " ", regex=True)
    text = text.str.lstrip()
    text = text.str.lower()
    return text.to_frame(name=column)


"""
Removing stopwords inside dataframe. Need install NLTK Stopwords to specify stopword list
"""


def remove_stopwords(dataframe, column: str, lang: str):
    from nltk.corpus import stopwords
    stop = stopwords.words({lang})
    data = dataframe[column].apply(lambda x: ' '.join([word for word in x.split() if word not in stop]))
    return data.to_frame(name=column)


"""
Tokenize using NLTK for split each word
"""


def generate_word(dataframe, column: str):
    data = dataframe[column].apply(word_tokenize)
    return data


"""
Change dataframe into id to word
"""


def id_to_word(dataframe):
    idto_word = corpora.Dictionary(dataframe)
    return idto_word


"""
Creating corpus by combine the id to word
"""


def corpus(dataframe):
    idtwords = corpora.Dictionary(dataframe)
    cps = []
    for text in df5:
        new = idtwords.doc2bow(text)
        cps.append(new)
    return cps


"""
Calling LDA model gensim
"""


def lda_model(corpuslda, id_two_w, topic: int, random_stat: int, update_every: int, chunksize: int, alpha="auto"):
    lda_mdl = gensim.models.ldamodel.LdaModel(corpus=corpuslda,
                                              id2word=id_two_w,
                                              num_topics=topic,
                                              random_state=random_stat,
                                              update_every=update_every,
                                              chunksize=chunksize,
                                              alpha=alpha)
    return lda_mdl


"""
Visualize the LDA model using pyLDAVis
"""


def visualize(lda_data, corpus_list, id2word_data, mds: str, r: int, filename):
    vis = pyLDAvis.gensim_models.prepare(topic_model=lda_data,
                                         corpus=corpus_list,
                                         dictionary=id2word_data,
                                         mds=mds,
                                         R=r)
    pyLDAvis.save_html(vis, f"{filename}.html")
    return vis


df = load_data("data.xlsx")
df2 = remove_username(df, "text")
df3 = cleaning_data(df2, "text")
df4 = remove_stopwords(df3, "text", "indonesian")
df5 = generate_word(df4, "text")
id2word = id_to_word(df5)
corpus_data = corpus(df5)
lda = lda_model(corpus_data, id2word, 7, 1, 2, 3)
visua = visualize(lda, corpus_data, id2word, "pcoa", 20, "testing2")

# THE DATASET NOT LEMMATIZE.TRY TO USE SPARKNLP FOR THAT
