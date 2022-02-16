import re
import gensim
import spacy
import pyLDAvis
import warnings
import pandas as pd
from gensim import corpora
import gensim.models.ldamodel
from nltk.corpus import stopwords
from pyLDAvis import gensim_models
from gensim.models import TfidfModel
from nltk.tokenize import word_tokenize

warnings.filterwarnings("ignore", category=DeprecationWarning)




def load_data(file):
    """
    Load_data fun reading excel file and change to ascii encoding for
    removing the emoji in dataframe
    """
    data = pd.read_excel(file)
    data = data.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
    return data


def remove_username(dataframe, column: str):
    """
    Removing username in dataframe.You should this before use cleaning_data function
    """
    final = []
    for text in dataframe[column].values.astype(str):
        text = re.sub(r'@[\w]+', '', text)
        final.append(text)
        data = pd.DataFrame(final, columns=[column])
    return data

def cleaning_data(dataframe, column: str):
    """
    Removing all character,symbol and etc in dataframe
    """
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

def remove_stopwords(dataframe, column: str, lang: str):
    """
    Removing stopwords inside dataframe. Need install NLTK Stopwords to specify stopword list
    """
    stop = stopwords.words({lang})
    data = dataframe[column].apply(lambda x: ' '.join([word for word in x.split() if word not in stop]))
    return data.to_frame(name=column)

def generate_word(dataframe, column: str):
    """
    Tokenize using NLTK for split each word
    """
    data = dataframe[column].apply(word_tokenize)
    return data

def id_to_word(dataframe):
    """
    Change dataframe into id to word
    """
    idto_word = corpora.Dictionary(dataframe)
    return idto_word

def create_corpus(dataframe,column:str):
    """
    Creating corpus by combine the id to word
    """

    generated = generate_word(dataframe,f"{column}")
    idtwords = corpora.Dictionary(generated)
    cps = []
    for text in generated:
        new = idtwords.doc2bow(text)
        cps.append(new)
    return cps

def lda_model(corpuslda, id_two_w, topic: int, random_stat: int, update_every: int, chunksize: int, alpha="auto"):
    """
    Calling LDA model gensim
    """
    lda_mdl = gensim.models.ldamodel.LdaModel(corpus=corpuslda,
                                              id2word=id_two_w,
                                              num_topics=topic,
                                              random_state=random_stat,
                                              update_every=update_every,
                                              chunksize=chunksize,
                                              alpha=alpha)
    return lda_mdl

def visualize(lda_data, corpus_list, id2word_data, mds: str, r: int, filename):
    """
    Visualize the LDA model using pyLDAVis
    """

    vis = pyLDAvis.gensim_models.prepare(topic_model=lda_data,
                                         corpus=corpus_list,
                                         dictionary=id2word_data,
                                         mds=mds,
                                         R=r)
    pyLDAvis.save_html(vis, f"{filename}.html")
    return vis

def remove_high_tfidf(dataframe,column:str,low_value:float):
    """
    USE THIS IF YOU HAVE A HIGH TFIDF WORD
    USE IT CAREFULLY FOR BACK UP CHECK MANUAL BOOK AT TXT
    THIS FUNCTION NEED CORPUS AND TFIDF
    :param dataframe: DATAFRAME YOU ARE USING
    :param column: COLUMN NAME
    :param low_value: MINIMUM OF VALUE
    :return:
    """
    generated_w = generate_word(dataframe,f"{column}")
    id2w = id_to_word(generated_w)
    corpustfidf = [id2w.doc2bow(text) for text in generated_w]
    tfidf = TfidfModel(corpustfidf, id2word=id2w)
    low_value = low_value
    words = []
    words_missing_in_tfidf = []

    for i in range(0, len(corpustfidf)):
        bow = corpustfidf[i]
        low_value_words = []  # reinitialize to be safe. You can skip this.
        tfidf_ids = [id for id, value in tfidf[bow]]
        bow_ids = [id for id, value in bow]
        low_value_words = [id for id, value in tfidf[bow] if value < low_value]
        drops = low_value_words + words_missing_in_tfidf
        for item in drops:
            words.append(id2w[item])
        words_missing_in_tfidf = [id for id in bow_ids if
                                  id not in tfidf_ids]  # The words with tf-idf socre 0 will be missing

        new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]
        corpustfidf[i] = new_bow
    return corpustfidf,id2w


df = load_data("data.xlsx")
df2 = remove_username(df, "text")
df3 = cleaning_data(df2, "text")
df4 = remove_stopwords(df3, "text", "indonesian")
df5 = generate_word(df4, "text") #key is on generated word for creating corpus and id2word
id2word = id_to_word(df5)
corpus_data = create_corpus(df4,"text")
corptfid = remove_high_tfidf(df4,"text",0.05)[0]
tfid2 = remove_high_tfidf(df4,"text",0.05)[1]
lda = lda_model(corptfid, tfid2, 7, 1, 2, 3)
visua = visualize(lda, corptfid, tfid2, "pcoa", 20, "tfid")


# THE DATASET NOT LEMMATIZE.TRY TO USE SPARKNLP FOR THAT
# REMEMBER TO SAVE THE MODEL USING gensim.save()





