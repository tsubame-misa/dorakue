"""
結果をboxplotやswarmplotで表示(最後にこれ使ってた)
"""


import glob
from networkx.readwrite import json_graph
import re
import json
from common import initGraph
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import networkx as nx



def crate_scatter_plt(x, y):
    plt.axhline(y=1, color='r', linestyle='--')
    plt.scatter(x, y, label='torus_maxd_y')

    plt.xlabel('times')
    plt.ylabel('compare stress')
    plt.title('')
    plt.legend()

    plt.show()

graph_set = [
    {"name":"Networkx", "torus":"honban_networkx_1014_20loop", "chen":"honban_networkx_1014_chen_20loop", "graph":"./graph_networkx_only/*", "s":3},
    {"name":"SuiteSparse Matrix", "torus":"honban_random_1014", "chen":"honban_random_1014_chen", "graph":"./randomGraphs/*", "s":3},
    {"name":"Real world", "torus":"honban_chen2020_1014_20loop", "chen":"honban_chen202_1014_chen_20loop", "graph":"./doughNetGraph/default/*", "s":4},
    # {"name":"Random Partition", "torus":"honban_chen2021_1014_20loop", "chen":"honban_chen2021_1014_chen_20loop", "graph":"./chen2021Graph/*", "s":3},
    {"name":"Random Partition2", "torus":"honban_chen2021_2_0105_20loop", "chen":"honban_chen2021_2_0105_chen_20loop", "graph":"./chen2021Graph2/*", "s":3},
]

with open("./modu2.json") as f:
    graph_detaiil = json.load(f)

box_data = {"edge_length_variance":[],"minimum_angle":[], "edge_crossings":[], "stress":[], "node_resolution":[]}
type_count = {"a":[], "b":[], "c":[], "d":[]}

for gs in graph_set:
    print(gs["name"])
    graphs = []
    for filepath in glob.glob(gs["graph"]):
        if filepath[-3:]=="txt" or filepath[-4:]=="test" or filepath[-3:]=="use":
            continue
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        if gs["name"] == "Random Partition2":
            file_name = graph.graph["name"]
        else:
            file_name = re.split('[/.]', filepath)[gs["s"]]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)

    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    result = []

    for g in sorted_graphs:
        # print(g["name"], "size", len(g["graph"].nodes))

        torus_log_file = glob.glob(gs["torus"]+"/log/"+g["name"]+'-best*')
        sgd_log_file = glob.glob(gs["chen"]+"/log/"+g["name"]+'-best*')

        with open(torus_log_file[0]) as f:
            torus_log = json.load(f)
        with open(sgd_log_file[0]) as f:
            sgd_log = json.load(f)

        maxd = initGraph.get_maxd(graph, file_name)

        type_count[graph_detaiil[gs["name"]][g["name"]]["type"]].append(gs["name"])

        stress_ratio = sgd_log["stress"]/torus_log["stress"]
        
        if stress_ratio < 1:
            print(gs["name"],g["name"], graph_detaiil[gs["name"]][g["name"]]["type"])
            continue
        
        for k in box_data:
            if k=="edge_crossings":
                v = (sgd_log["edge_crossings"]+1)/(torus_log["edge_crossings"]+1)
            else:
                v = sgd_log[k]/torus_log[k]

            if k!="node_resolution" and v > 10:
                continue
            box_data[k].append({"value": v, "graph set":gs["name"], "type":graph_detaiil[gs["name"]][g["name"]]["type"], 
                                    # "modularity":graph_detaiil[gs["name"]][g["name"]]["modularity"],  
                                    "diameter":graph_detaiil[gs["name"]][g["name"]]["diameter"]})

    type_result = []


for t in type_count:
    print(t, len(type_count[t]))

print(type_count)
    
for key in ["edge_length_variance","minimum_angle", "edge_crossings", "stress", "node_resolution"]:

    df = pd.DataFrame(box_data[key])
    order = ["a", "b", "c"]


    # Swarm plot
    plt.figure(figsize=(10, 6))  # 図のサイズを調整
    #sns.boxplot(x='type', y='value', data=df, palette=sns.color_palette('Set2', n_colors=len(df['type'].unique())), order=order)
    
    # sns.boxplot(x='type', y='value', data=df, color='white', order=order, width=0.5, sym="")
    # plt.axhline(y=1, color='blue', linestyle='--', label='value=1')

    # sns.scatterplot(x='diameter', y='value', data=df, hue='graph set')

    # sns.swarmplot(x="diameter", y='value', data=df, hue='graph set', alpha=0.7)

    sns.swarmplot(x="diameter", y='value', data=df, hue="type", hue_order=order, alpha=0.7)

    plt.ylabel(key)
    # plt.legend()

    # グラフの表示
    # plt.show()