import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
import os
import shutil
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_hub as text
from official.nlp import optimization  # to create AdamW optimizer

import matplotlib.pyplot as plt
df = pd.read_excel("data_training.xlsx")
dfg = df.groupby('label').count()
fig = px.bar(dfg,x="text",title='Distribution')


#