import networkx as nx
import os
import json
import matplotlib.pyplot as plt
import setup
from common import log,  drawGraph 
from algorithm.SGDBase import egraphTorusSGD
import egraphSearchBestGraphByAvarage

new_dir_path = './chen2021Graph2/'

if not os.path.isdir(new_dir_path):
    os.mkdir(new_dir_path)

node = 10
group = 30
p_in = 0.75
p_out = 0.001
name = str(node)+"-"+str(group)+"-"+str(p_in)+"-"+str(p_out)


G = nx.random_partition_graph([node] * group, p_in=p_in, p_out=p_out) 

undirected_G = G.to_undirected()
largest_cc = max(nx.connected_components(undirected_G), key=len)
largest_sub_graph = undirected_G.subgraph(largest_cc).copy()
scale_free_graph = nx.Graph(largest_sub_graph)
for j in scale_free_graph.nodes:
    if scale_free_graph.has_edge(j,j):
        scale_free_graph.remove_edge(j,j)
data = nx.node_link_data(scale_free_graph)
nx.draw_networkx(scale_free_graph, node_size=5, with_labels=None, width=0.5)

# comp = nx.community.girvan_newman(scale_free_graph)
# a = tuple(sorted(c) for c in next(comp))
# m = nx.community.modularity(scale_free_graph, a)

# print(m)

plt.show()

n_data = dict()
for k in data.keys():
    if k == "graph":
        n_data["graph"] = {"name":name}
    if k in ["directed","multigraph","links"]:
        n_data[k] = data[k] 
    if k == "nodes":
        n_data["nodes"] = []
        for node in data["nodes"]:
            n_data["nodes"].append({"id":node["id"]})


box_data = dict()

# setup.set_dir_name("uuu")
# log.create_log_folder()


# time = setup.get_time()
# index_time = str(0) + str(time)
# drawGraph.set_time(index_time)
# chen_log =  egraphTorusSGD.torus_sgd(scale_free_graph, name+"chen", 1.5, 0, index_time, True)
# our_log = egraphSearchBestGraphByAvarage.search_min_stress_len(scale_free_graph, name, 1)

# for k in ["edge_length_variance","minimum_angle", "edge_crossings", "stress", "node_resolution"]:
#     if k=="edge_crossings":
#         v = (chen_log["edge_crossings"]+1)/(our_log["edge_crossings"]+1) 
#     else:
#         v = chen_log[k]/our_log[k]
#     box_data[k] = v

# print(box_data)
# save_log ={"ratio":box_data,"our":our_log, "chen":chen_log}
# log.create_log(save_log, name)



with open(new_dir_path + name+ ".json", "w") as f:
    json.dump(n_data, f)


