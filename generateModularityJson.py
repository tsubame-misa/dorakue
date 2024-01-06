"""
グラフの基本情報データの作成(モジュラリティを求める)
"""


import glob
from networkx.readwrite import json_graph
import json
import matplotlib.pyplot as plt
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
    # {"name":"test_m_graph", "graph":"./test_m_graph/*"},
    # {"name":"Networkx", "torus":"honban_networkx_1014_20loop", "chen":"honban_networkx_1014_chen_20loop", "graph":"./graph_networkx_only/*", "s":3},
    # {"name":"Real world", "torus":"honban_chen2020_1014_20loop", "chen":"honban_chen202_1014_chen_20loop", "graph":"./doughNetGraph/default/*", "s":4},
    # {"name":"Random Partition", "torus":"honban_chen2021_1014_20loop", "chen":"honban_chen2021_1014_chen_20loop", "graph":"./chen2021Graph/*", "s":3},
    # {"name":"SuiteSparse Matrix", "torus":"honban_random_1014", "chen":"honban_random_1014_chen", "graph":"./randomGraphs/*", "s":3},
    {"name":"Random Partition", "torus":"honban_chen2021_2_0105_20loop", "chen":"honban_chen2021_2_0105_chen_20loop", "graph":"./chen2021Graph2/*", "s":3},
]

modu_dic = dict()

for gs in graph_set:
    print(gs["name"])
    graphs = []
    for filepath in glob.glob(gs["graph"]):
        if filepath[-3:]=="txt" or filepath[-4:]=="test":
            continue
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        
        comp = nx.community.girvan_newman(graph)
        a = tuple(sorted(c) for c in next(comp))
        m = nx.community.modularity(graph, a)
        # file_name = re.split('[/.]', filepath)[gs["s"]]
        file_name = graph.graph["name"]
        if not gs["name"] in modu_dic:
            modu_dic[gs["name"]] = dict()
        modu_dic[gs["name"]][file_name] = {"modularity":m}

# 更新したデータをJSONファイルに書き込む
with open("modu3.json", 'w') as file:
    json.dump(modu_dic, file)