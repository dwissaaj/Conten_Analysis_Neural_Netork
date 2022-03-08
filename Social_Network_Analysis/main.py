import pandas as pd
from pyvis.network import Network
import matplotlib.pyplot as plt
import networkx as nx


nt = Network()
df = pd.read_excel("Book1.xlsx")
nodes = list(set(df["vertex1"]).union(df["vertex2"]))
data2 = df["vertex1"].to_list()
data3 = df["vertex2"].to_list()
edges = [list(l) for l in zip(data2,data3)]
nt.add_nodes(nodes)
nt.add_edges(edges)

G = nx.Graph()
G.add_edges_from(list(zip(df["vertex1"],df["vertex2"])))
cluster = nx.clustering(G)
nx.draw(cluster)
plt.show()


"""
G.add_edges_from(zip(vertex1,vertex2))
nx.draw(G)
plt.show()
nt = Social_Network_Analysis()
"""