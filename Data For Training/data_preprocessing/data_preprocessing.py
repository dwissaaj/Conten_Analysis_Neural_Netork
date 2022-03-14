import json
import re
import warnings
import pandas as pd
from wordsegment import load, segment
from nltk.corpus import stopwords
load()
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

def cleaning_data(dataframe, column: str,hastag_return: bool):
    """
    Removing all character,symbol and etc in dataframe
    """
    hastag = dataframe[column].apply(lambda x: re.findall(r'\B#\w*[a-zA-Z]+\w*', x))
    text = dataframe[column].str.replace(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', regex=True)
    text = text.str.replace(r'#(\w+)','',regex=True)
    text = text.str.replace(r'[\/]','',regex=True)
    text = text.str.replace(r'[%]','',regex=True)
    text = text.str.replace(r'[()]','',regex=True)
    text = text.str.replace(r'[(]','',regex=True)
    text = text.str.replace(r'[)]','',regex=True)
    text = text.str.replace(r'[-]','',regex=True)
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
        return pd.concat([text,hastag],axis=1)
    else:
        return text.to_frame(name=column)

def remove_stopwords(dataframe, column: str, lang = "indonesian"):
    """
    Removing stopwords inside dataframe. Need install NLTK Stopwords to specify stopword list
    """
    stop = stopwords.words({lang})
    data = dataframe[column].apply(lambda x: ' '.join([word for word in x.split() if word not in stop]))
    data = data.drop_duplicates()
    return data.to_frame(name=column)

def write_json(filename:str,dataframe):
    with open(f'{filename}.json', 'w') as f:
        f.write(dataframe.to_json(orient="records", lines=False))



df = load_data("Book1.xlsx")
df3 = remove_username(df,"text")
df4 = remove_stopwords(df3,"text","indonesian")
df5 = cleaning_data(df4,"text",False)
df6 = df5.replace({"biznet":"",
                   "indihome":"",
                   "indosat":"",
                   "smartfren":"",
                   "first media":"",
                   "\_":"",
                   "myrepublic":"",
                   "firstmedia":""},regex=True)
write_json("data3",df6)
