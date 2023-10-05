import json
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from matplotlib import collections
from networkx.readwrite import json_graph
import itertools


def create_pos9(pos, _len):
    add_len = [-_len, 0, _len]
    pos9 = []
    for p in pos:
        for w in add_len:
            for h in add_len:
                pos9.append([p[0]+w, p[1]+h])
    return pos9


def max_dict(pos):
    max_d = 0
    for p0, p1 in itertools.combinations(pos, 2):
        d = ((p0[0]-p1[0])**2+(p0[1]-p1[1])**2)**0.5
        if d > max_d:
            max_d = d
    return max_d


def draw_node(pos, ax):
    for p in pos:
        C = pat.Circle(xy=(p[0], p[1]), radius=2.5, color="blue")
        ax.add_patch(C)


def draw_edge(graph, node2num,  pos, l,  _len, ax, debug=False):
    edge_lines = []
    wrap_lines = []
    wrap_lines2 = []

    for i, j in graph.edges:
        idx_i = node2num[str(i)]
        idx_j = node2num[str(j)]

        best_pos, is_wrap = select_node(
            pos, idx_i, idx_j, _len, l[idx_i][idx_j])

        if is_wrap:
            line = [(pos[idx_i][0], pos[idx_i][1]),
                    (best_pos[0], best_pos[1])]
            if debug:
                wrap_lines.append(line)
            else:
                edge_lines.append(line)

            best_pos, is_wrap = select_node(
                pos,  idx_j, idx_i, _len, l[idx_i][idx_j])
            line = [(pos[idx_j][0], pos[idx_j][1]),
                    (best_pos[0], best_pos[1])]
            if debug:
                wrap_lines2.append(line)
            else:
                edge_lines.append(line)
        else:
            line = [(pos[idx_i][0], pos[idx_i][1]),
                    (pos[idx_j][0], pos[idx_j][1])]
            edge_lines.append(line)

    if debug:
        line_collection = collections.LineCollection(
            edge_lines, color=("green",), linewidths=(0.5,))
    else:
        line_collection = collections.LineCollection(
            edge_lines, color=("blue",), linewidths=(0.5,))
    ax.add_collection(line_collection)

    line_collection = collections.LineCollection(
        wrap_lines, color=("red",), linewidths=(0.5,))
    ax.add_collection(line_collection)

    line_collection = collections.LineCollection(
        wrap_lines2, color=("orange",), linewidths=(0.5,))
    ax.add_collection(line_collection)


def select_node(pos, u, v, _len, ideal_dist):
    # uから見た
    x_list = [pos[v][0]-_len, pos[v][0], pos[v][0]+_len]
    y_list = [pos[v][1]-_len, pos[v][1], pos[v][1]+_len]

    best_pos = [pos[v][0], pos[v][1]]
    _dist = float("inf")

    for x in x_list:
        for y in y_list:
            ax = pos[u][0] - x
            ay = pos[u][1] - y
            adist = (ax ** 2 + ay ** 2) ** 0.5
            if abs(_dist-ideal_dist) > abs(adist-ideal_dist):
                best_pos[0] = x
                best_pos[1] = y
                _dist = adist

    is_wrap = not(best_pos[0] == pos[v][0] and best_pos[1] == pos[v][1])

    return best_pos, is_wrap


def graph_drawing(data, graph, _len, file_path, debug=False):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    ax.tick_params(labelbottom=True, labelleft=True,
                   labelright=False, labeltop=False, bottom=False, left=False, right=False, top=False)

    print("d", max_dict(data["pos"]))

    if debug:
        ax.set_xlim(-_len, _len*2)
        ax.set_ylim(-_len, _len*2)

        # セルのライン
        cell_lines = [[(0, -_len), (0, _len*2)], [(_len, -_len),
                                                  (_len, _len*3)], [(-_len, 0), (_len*2, 0)], [(-_len, _len), (_len*2, _len)]]
        line_collection = collections.LineCollection(
            cell_lines, color=("black",), linewidths=(0.5,))
        ax.add_collection(line_collection)
    else:
        ax.set_xlim(0, _len)
        ax.set_ylim(0, _len)

    pos9 = create_pos9(data["pos"], _len)
    draw_node(pos9, ax)
    draw_edge(graph, data["node2num"], data["pos"], data["l"], _len, ax, debug)

    plt.savefig(file_path)
    plt.clf()
    plt.close()


with open("./result_1005/log/qh882-20231005011753.json") as f:
    data = json.load(f)
    # 020231005011753
    # s005011753
    data = data["6200"]["020231005011753"]["torusSGD"]
    graph = json_graph.node_link_graph(
        json.load(open("./graph/qh882.json")))
    _len = 6200

    graph_drawing(data, graph, _len, "./sample_qh882.png")
