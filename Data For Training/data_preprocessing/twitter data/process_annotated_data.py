import pandas as pd
def load_json(file):
    dataframe = pd.read_json(f'{file}',lines=True)
    return dataframe

df1 = load_json("sen_data.jsonl")
df2 = load_json("sentiment.jsonl")
df3 = load_json("sentiment2.jsonl")
df4 = load_json("sentiment3.jsonl")

df1.to_excel("df1.xlsx")
df2.to_excel("df2.xlsx")
df3.to_excel("df3.xlsx")
df4.to_excel("df4.xlsx")