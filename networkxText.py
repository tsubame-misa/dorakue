import matplotlib.pyplot as plt
import networkx as nx
import json
import networkx as nx
from networkx.readwrite import json_graph
import glob

files = glob.glob("./tmp/*")
for file in files:
    print(file)

filename = 'graph/bull.json'
graph = json_graph.node_link_graph(json.load(open(filename)))

print(graph)
# ノードの一覧
print(graph.nodes)
# エッジの一覧
print(graph.edges)


G = nx.DiGraph()

G.add_nodes_from(graph.nodes)
G.add_edges_from(graph.edges)

nx.draw_networkx(G)
plt.show()


# G = nx.DiGraph()
# nx.add_path(G, [3, 5, 4, 1, 0, 2, 7, 8, 9, 6])
# nx.add_path(G, [3, 0, 6, 4, 2, 7, 1, 9, 8, 5])


# pos = dict()

# for i in range(10):
#     pos[i] = [i, i]

# print(pos)

# nx.draw_networkx(G, pos)
# plt.show()

# G = nx.path_graph(4)
# pos = nx.circular_layout(G)
# print(pos)


"""
pos = {0: array([9.99999986e-01, 2.18556937e-08]), 1: array([-3.57647606e-08,  1.00000000e+00]), 2: array([-9.9999997e-01, -6.5567081e-08]), 3: array([ 1.98715071e-08, -9.99999956e-01])}
"""
