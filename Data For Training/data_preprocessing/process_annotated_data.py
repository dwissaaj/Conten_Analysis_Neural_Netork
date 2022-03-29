import sys

import pandas as pd

sys.path.append("../Thesis/ModulFunc")

from ModulFunc import funcm

functi = funcm.functions()
df = functi.load_data("../data_preprocessing/raw_data.xlsx")
text = df[['text']]
text = text.replace('\n','', regex=True)
text = text["text"].str.lower()
data = pd.DataFrame(text)
functi.write_json("ig_dat.xlsx",data)