import json
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from matplotlib import collections
from networkx.readwrite import json_graph


def create_pos9(pos, _len):
    add_len = [0, _len, _len*2]
    pos9 = []
    for p in pos:
        for w in add_len:
            for h in add_len:
                pos9.append([p[0]+w, p[1]+h])
    return pos9


def draw_node(pos, ax):
    for p in pos:
        C = pat.Circle(xy=(p[0], p[1]), radius=2.5, color="blue")
        ax.add_patch(C)


def draw_edge(graph, node2num,  pos, _len, ax):
    edge_lines = [[(_len, 0), (_len, _len*3)], [(_len*2, 0),
                                                (_len*2, _len*3)], [(0, _len), (_len*3, _len)], [(0, _len*2), (_len*3, _len*2)]]

    for i, j in graph.edges:
        idx_i = node2num[str(i)]
        idx_j = node2num[str(j)]

        line = [(pos[idx_i][0], pos[idx_i][1]), (pos[idx_j][0], pos[idx_j][1])]
        edge_lines.append(line)

    line_collection = collections.LineCollection(
        edge_lines, color=("green",), linewidths=(0.5,))
    ax.add_collection(line_collection)


def graph_drawing(graph, pos, _len):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, _len*3)
    ax.set_ylim(0, _len*3)

    cell_lines = [[(_len, 0), (_len, _len*3)], [(_len*2, 0),
                                                (_len*2, _len*3)], [(0, _len), (_len*3, _len)], [(0, _len*2), (_len*3, _len*2)]]
    line_collection = collections.LineCollection(
        cell_lines, color=("black",), linewidths=(0.5,))
    ax.add_collection(line_collection)

    draw_node(pos, ax)
    draw_edge(graph, data["node2num"], pos, _len, ax)

    plt.savefig("./sample.png")
    plt.clf()
    plt.close()


with open("./result_sgd_0725_all_log/log/desargues-20230724233845.json") as f:
    data = json.load(f)
    data = data["500"]["920230724233805"]["torusSGD"]
    graph = json_graph.node_link_graph(
        json.load(open("./graph/desargues.json")))
    _len = 500

    # pos9 = create_pos9(data["pos"], _len)
    pos9 = data["pos"]

    graph_drawing(graph, pos9, _len)
