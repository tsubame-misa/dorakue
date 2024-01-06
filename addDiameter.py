"""
グラフの基本情報データの作成(シートに直径を追加)
"""

import glob
from networkx.readwrite import json_graph
import json
import networkx as nx

graph_set = [
    # {"name":"test_m_graph", "graph":"./test_m_graph/*"},
    # {"name":"Networkx", "torus":"honban_networkx_1014_20loop", "chen":"honban_networkx_1014_chen_20loop", "graph":"./graph_networkx_only/*", "s":3},
    # {"name":"Real world", "torus":"honban_chen2020_1014_20loop", "chen":"honban_chen202_1014_chen_20loop", "graph":"./doughNetGraph/default/*", "s":4},
    # {"name":"Random Partition", "torus":"honban_chen2021_1014_20loop", "chen":"honban_chen2021_1014_chen_20loop", "graph":"./chen2021Graph/*", "s":3},
    # {"name":"SuiteSparse Matrix", "torus":"honban_random_1014", "chen":"honban_random_1014_chen", "graph":"./randomGraphs/*", "s":3},
     {"name":"Random Partition2", "torus":"honban_chen2021_2_0105_20loop", "chen":"honban_chen2021_2_0105_chen_20loop", "graph":"./chen2021Graph2/*", "s":3},
]

with open("./modu2.json") as f:
    data = json.load(f)


for gs in graph_set:
    print(gs["name"])
    graphs = []
    for filepath in glob.glob(gs["graph"]):
        if filepath[-3:]=="txt" or filepath[-4:]=="test":
            continue
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        diameter = nx.diameter(graph)

        # file_name = re.split('[/.]', filepath)[gs["s"]]
        file_name = graph.graph["name"]
        print(file_name)
        data[gs["name"]][file_name]["diameter"] = diameter
        data[gs["name"]][file_name]["type"] = "b"

# 更新したデータをJSONファイルに書き込む
with open("modu2.json", 'w') as file:
    json.dump(data, file)