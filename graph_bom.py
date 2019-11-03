import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import json


def tokenize(df, cols):
    cols = list(cols)
    unique_values = np.unique(df[cols].to_numpy())
    tokens = np.arange(0, unique_values.shape[0])
    df_tokens = pd.DataFrame({"val": unique_values, "tokens": tokens})
    node_cols = list()
    for i in cols:
        token_col_name = "%s_prime" % i
        df = df.merge(df_tokens, left_on=i, right_on='val', how='left')
        df = df.rename({'tokens': token_col_name}, axis=1)
        df.drop('val', axis=1, inplace=True)
        node_cols.append(token_col_name)
    attrs = dict(zip(df_tokens.tokens, df_tokens.val))
    return df, attrs


def duplicate_node_copy(G):
    in_degree = list(G.in_degree)
    in_degree_gte_2 = list(filter(lambda x: x[1] >= 2, in_degree))
    for i in in_degree_gte_2:
        target_node, deg = i
        predecessors = list(G.predecessors(target_node))
        for j in predecessors[1:]:
            new_node = len(G.nodes)
            old_node_data = G.nodes[target_node]
            G.remove_edge(j, target_node)
            G.add_edge(j, new_node)
            G.nodes[new_node].update(old_node_data)
    return G


df = pd.read_excel("assets/sample_bom.xlsx")
df_tokenized, attrs = tokenize(df, ['parent', 'child'])
print(attrs)
G = nx.convert_matrix.from_pandas_edgelist(df_tokenized, 'parent_prime', 'child_prime', create_using=nx.DiGraph)
for i, j in attrs.items():
    G.nodes[i].setdefault('name', j)
H = nx.bfs_tree(G, 3)
H1 = G.subgraph(H)
nx.draw_networkx(H)
plt.show()

G_prime = duplicate_node_copy(G)


data = nx.readwrite.json_graph.tree_data(G_prime, 4, {'id': 'token', 'children': 'children'})
with open('output/sample_bom.json', 'w') as file:
    json.dump(data, file)