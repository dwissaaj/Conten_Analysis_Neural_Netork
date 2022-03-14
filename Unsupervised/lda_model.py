import re
import warnings

import gensim
import gensim.models.ldamodel
import matplotlib.pyplot as plt
import pandas as pd
import pyLDAvis
from gensim import corpora
from gensim.models import TfidfModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pyLDAvis import gensim_models
from wordcloud import WordCloud

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


def cleaning_data(dataframe, column: str, hastag_return: bool):
    """
    Removing all character,symbol and etc in dataframe
    """
    hastag = dataframe[column].apply(lambda x: re.findall(r'\B#\w*[a-zA-Z]+\w*', x))
    text = dataframe[column].str.replace(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', regex=True)
    text = text.str.replace(r'#(\w+)', '', regex=True)
    text = text.str.replace(r"[\"\'\|\?\=\.\\*\+\!\:\,]", '', regex=True)
    text = text.str.replace(r'\d+', '', regex=True)
    text = text.str.replace(r'RT', '', regex=True)
    text = text.str.replace(r'\n', ' ', regex=True)
    text = text.str.replace(r'\s\s+', " ", regex=True)
    text = text.str.lstrip()
    text = text.str.lower()
    if hastag_return == True:
        hastag = hastag.to_frame(name="hastag")
        text = text.to_frame(name=column)
        return pd.concat([text, hastag], axis=1)
    else:
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


def create_corpus(dataframe, column: str):
    """
    Creating corpus by combine the id to word
    """

    generated = generate_word(dataframe, f"{column}")
    idtwords = corpora.Dictionary(generated)
    cps = []
    for text in generated:
        new = idtwords.doc2bow(text)
        cps.append(new)
    return cps


def lda_model(corpuslda, id_two_w, topic: int):
    """
    Calling LDA model gensim
    """
    lda_mdl = gensim.models.ldamodel.LdaModel(corpus=corpuslda,
                                              id2word=id_two_w,
                                              num_topics=topic
                                             )
    return lda_mdl


def visualize(lda_data, corpus_list, id2word_data, mds: str, r: int,filename:str):
    """
    Visualize the LDA model using pyLDAVis
    """

    vis = pyLDAvis.gensim_models.prepare(topic_model=lda_data,
                                         corpus=corpus_list,
                                         dictionary=id2word_data,
                                         mds=mds,
                                         R=r)
    pyLDAvis.save_html(vis,f"{filename}.html")
    return vis


def remove_high_tfidf(dataframe, column: str, low_value: float):
    """
    USE THIS IF YOU HAVE A HIGH TFIDF WORD
    USE IT CAREFULLY FOR BACK UP CHECK MANUAL BOOK AT TXT
    THIS FUNCTION NEED CORPUS AND TFIDF
    :param dataframe: DATAFRAME YOU ARE USING
    :param column: COLUMN NAME
    :param low_value: MINIMUM OF VALUE
    :return:
    """
    generated_w = generate_word(dataframe, f"{column}")
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
    return corpustfidf, id2w


def to_json(filename: str, dataframe):
    with open(f'{filename}.json', 'w') as f:
        f.write(dataframe.to_json(orient="records"))

def get_hastag(dataframe,column:str)-> list:
    nan_value = float("NaN")
    dataframe[column] = dataframe[column].apply(lambda x: re.findall(r'\B#\w*[a-zA-Z]+\w*', x))
    hastag = dataframe.astype(str).drop_duplicates()
    hastag = hastag.replace({"\[": "",
                          "\]": "",
                          "\'": "",
                          "\,": " "}, regex=True)
    hastag.replace("", nan_value, inplace=True)
    hastag.dropna(subset = [column], inplace=True)
    tagstr = hastag[column].values.tolist()
    return tagstr

def wordcloud_maker(stack:list,colormap:str):
    to_str = ' '.join(map(str,stack))
    wordcloud = WordCloud(width=2000, height=2000,max_words=75, colormap=f"{colormap}").generate(to_str)
    plt.figure()
    plt.imshow(wordcloud, interpolation="lanczos")
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()



df = load_data("Voxpopdata.xlsx")
remove_user = remove_username(df,"text")
clean_data = cleaning_data(remove_user,"text",False)
remove_stop = remove_stopwords(clean_data,"text","indonesian")
toenize = generate_word(clean_data,"text")
id2word = id_to_word(toenize)
corpus = create_corpus(remove_stop,"text")


ldah = lda_model(corpus,id2word,25 )
hastag = get_hastag(df,"text")
wordcloud_maker(hastag,"Set2")


""""
lowcor = remove_high_tfidf(clean_data,"text",0.1)[0]
lowid = remove_high_tfidf(clean_data,"text",0.1)[1]
ldal = lda_model(lowcor,lowid,25 )
viz2 = visualize(ldal,corpus,id2word,"mmds",1,"pemilul6")
"""
wd = wordcloud_maker(hastag,"Set1")
#vish = visualize(lda,corpus,id2word,"mmds",10,"normal")

