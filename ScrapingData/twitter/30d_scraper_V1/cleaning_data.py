import re
import pandas as pd


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
    text = dataframe[column].str.replace(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', regex=True)
    text = text.str.replace(r"[\"\'\|\?\=\.\\#\*\+\!\:\,]", '', regex=True)
    text = text.str.replace(r'\d+', '', regex=True)
    text = text.str.replace(r'RT', '', regex=True)
    text = text.str.replace(r'\n', ' ', regex=True)
    text = text.str.replace(r'\s\s+', " ", regex=True)
    text = text.str.lstrip()
    text = text.str.lower()
    return text.to_frame(name=column)

loading = load_data("clean_data/text_data.xlsx")
remove_us = remove_username(loading,"text")
clean_data = cleaning_data(remove_us,"text")
clean_data.to_excel("..\data_30_days\data_clean.xlsx")