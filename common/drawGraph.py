import matplotlib.pyplot as plt
import networkx as nx
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import re


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
    img_path = get_dir()+'/result/compare/' + name + \
        "-" + size[1] + "-" + TIME + '.png'
    plt.savefig(img_path)

    plt.clf()
    plt.close()


def create_and_save_graph(graph, pos, node_color, edge_color, dir_name, width, height, name=""):
    G = nx.DiGraph()

    G.add_nodes_from(graph.nodes)
    G.add_edges_from(graph.edges)

    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G, pos, False,
                     node_color=node_color, edge_color=edge_color, node_size=50, font_size=5)

    img_path = get_dir()+'/result/' + dir_name + '/' + \
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
