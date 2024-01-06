import glob
import json
from networkx.readwrite import json_graph
from common import drawGraph, drawEgraph
import networkx as nx
import matplotlib.pyplot as plt
import setup


def create_graph(pos, graph):
    G = nx.DiGraph()

    G.add_nodes_from(graph.nodes)
    G.add_edges_from(graph.edges)

    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G, pos, False, with_labels=False,
                        node_color="#88888899", edge_color="#888888", node_size=200, font_size=5)

    img_path = "sample-torus.png"
    plt.savefig(img_path)
    plt.clf()
    plt.close()


def convert_pos(log_pos):
    pos =  dict()
    for p in log_pos:
        if p[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            pos[int(p)] = log_pos[p]
        else:
            pos[p] = log_pos[p]
    return pos

filepath = "honban_chen2020_1014_20loop/log/13-best-.json"
# filepath = "./test_stress_liner_avarage_20/log/icosahedral-.json"
graph_file = "doughNetGraph/default/13.json"

graph = json_graph.node_link_graph(json.load(open(graph_file)))

with open(filepath) as f:
    _log = json.load(f)

pos = convert_pos(_log["pos"])

# create_graph(pos ,graph)
setup.set_dir_name("uuu")
drawEgraph.torus_graph_drawing(pos, graph, "13", 1, time="xxx", debug=False)
