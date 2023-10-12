import matplotlib.pyplot as plt
import networkx as nx
import plotly.express as px
import matplotlib.image as mpimg
import os
import re
import setup
import matplotlib.patches as pat
from matplotlib import collections
import itertools


list_colors = px.colors.sequential.Plasma
IMAGE_PATH = []
TIME = ""


def set_time(time):
    global TIME
    TIME = time


def clear():
    global IMAGE_PATH, TIME
    IMAGE_PATH = []
    TIME = ""


def get_dir():
    cwd = os.getcwd()
    return cwd


def create_compare_fig(name=""):
    fig = plt.figure(figsize=(12, 12))
    for i in range(len(IMAGE_PATH)):
        ax = fig.add_subplot(2, 3, i+1)

        title = IMAGE_PATH[i].split("/")
        ax.set_title(title[9], fontsize=10)
        ax.axes.xaxis.set_visible(False)  # X軸を非表示に
        ax.axes.yaxis.set_visible(False)  # Y軸を非表示に

        img = mpimg.imread(IMAGE_PATH[i])
        plt.imshow(img)

        size = title[10].split("-")
    dir_name = setup.get_dir_name()
    img_path = get_dir()+'/'+dir_name+'/compare/' + name + \
        "-" + size[1] + "-" + TIME + '.png'
    plt.savefig(img_path)

    plt.clf()
    plt.close()


def create_and_save_graph(graph, pos, node_color, edge_color, alg_dir_name, width, height, name=""):
    G = nx.DiGraph()

    G.add_nodes_from(graph.nodes)
    G.add_edges_from(graph.edges)

    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G, pos, False,
                     node_color=node_color, edge_color=edge_color, node_size=50, font_size=5)

    dir_name = setup.get_dir_name()

    img_path = get_dir()+'/'+dir_name+'/' + alg_dir_name + '/' + \
        str(name) + '-' + str(height) + '-' + TIME + '.png'
    plt.savefig(img_path)
    IMAGE_PATH.append(img_path)

    plt.clf()
    plt.close()


def get_color(delta, node_len):
    # delta01 = preprocessing.minmax_scale(delta).tolist()
    color = []
    for i in range(node_len):
        color.append(list_colors[0])
        continue
        c_idx = int(delta01[i]*10)
        if c_idx >= len(list_colors):
            c_idx = len(list_colors)-1
        color.append(list_colors[c_idx])
    return color


def get_graph_color(graph):
    # delta01 = preprocessing.minmax_scale(delta).tolist()
    color = []
    for i in range(len(graph.nodes)):
        color.append(list_colors[graph.nodes[i]["tier"]*3])
    return color


def convert_graph_dict(nodes, pos):
    dict_pos = {}
    cnt = 0
    for node in nodes:
        dict_pos[node] = pos[cnt]
        cnt += 1
    return dict_pos


def draw_graph(graph, pos, delta, edge_score, node_len, dir_name, width, height, file_name=""):
    node_color = get_color(delta, node_len)
    # node_color = get_graph_color(graph)
    edge_color = get_color(edge_score, node_len)
    # グラフ描画
    dict_pos = convert_graph_dict(graph.nodes, pos)
    create_and_save_graph(graph, dict_pos,  node_color, edge_color,
                          dir_name, width, height, file_name)


def get_single_alg_figs(file_name, image_paths):
    fig = plt.figure(figsize=(12, 12))
    for i in range(len(image_paths)):
        time = re.split('[_./-]', image_paths[i])[-2]
        ax = fig.add_subplot(3, 4, i+1)
        ax.axes.xaxis.set_visible(False)  # X軸を非表示に
        ax.axes.yaxis.set_visible(False)  # Y軸を非表示に
        img = mpimg.imread(image_paths[i])
        ax.set_title(time, fontsize=10)
        plt.imshow(img)
    img_path = get_dir()+'/comp_result/single/img/' + file_name + '.png'
    # plt.title(file_name, loc='center', fontsize=30,  pad=30)
    fig.suptitle(file_name, fontsize=30)
    plt.savefig(img_path)


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


def torus_graph_drawing(pos, l, node2num, graph, _len, alg_dir_name, name, debug=False):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    ax.tick_params(labelbottom=False, labelleft=False,
                   labelright=False, labeltop=False, bottom=False, left=False, right=False, top=False)

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

    pos9 = create_pos9(pos, _len)
    draw_node(pos9, ax)
    draw_edge(graph, node2num, pos, l, _len, ax, debug)

    dir_name = setup.get_dir_name()

    img_path = get_dir()+'/'+dir_name+'/' + alg_dir_name + '/' + \
        str(name) + '-' + str(_len) + '-' + TIME + '.png'
    plt.savefig(img_path)
    IMAGE_PATH.append(img_path)

    plt.clf()
    plt.close()
