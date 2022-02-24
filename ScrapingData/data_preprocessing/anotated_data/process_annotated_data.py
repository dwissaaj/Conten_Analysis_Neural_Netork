import pandas as pd
def load_json(file):
    dataframe = pd.read_json(f'{file}',lines=True)
    return dataframe
