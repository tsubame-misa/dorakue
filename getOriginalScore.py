import json
import glob
import re
import os
from common import drawGraph, log, calcDrawInfo,  initGraph, aestheticsMeasures, debug
from networkx.readwrite import json_graph
import networkx as nx
import matplotlib.pyplot as plt
import setup


def draw_graph(graph, pos, name):
    G = nx.DiGraph()

    G.add_nodes_from(graph.nodes)
    G.add_edges_from(graph.edges)

    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G, pos, False, node_size=50, font_size=5)

    img_path = "./doughNetGraph/origin/img/" + name + '.png'
    plt.savefig(img_path)

    plt.clf()
    plt.close()


for filepath in glob.glob("./doughNetGraph/default/*"):
    with open(filepath) as f:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        filename = re.split('[/.-]', filepath)[-2]
        path = os.getcwd()

    with open("./doughNetGraph/pos_only/" + filename + ".json") as f:
        pos = json.load(f)["pos"]

    node_len = len(graph.nodes)
    node2num = initGraph.get_node2num_memoized(graph)
    d = initGraph.get_shortest_path(graph, node_len, node2num, filename)
    # l=1のため最短経路と一致
    l = [[0]*node_len for i in range(node_len)]
    k = [[0]*node_len for i in range(node_len)]

    for _i in graph.nodes:
        for _j in graph.nodes:
            i = node2num[str(_i)]
            j = node2num[str(_j)]
            if i == j:
                continue
            k[i][j] = 1/(d[_i][_j]*d[_i][_j])
            l[i][j] = d[_i][_j]

    delta = calcDrawInfo.calc_delta(pos, k, l, node_len)
    edge_score = [(d[u][v] -
                   calcDrawInfo.dist(pos, node2num[str(u)], node2num[str(v)]))**2 for u, v in graph.edges]

    _log = aestheticsMeasures.calc_evaluation_values(
        delta, edge_score, graph, node2num, pos, l)

    path = os.getcwd()

    with open(path + "/doughNetGraph/score/" + filename+".json", "w") as f:
        json.dump(_log, f)

    draw_graph(graph, pos, filename)
