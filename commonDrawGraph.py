import matplotlib.pyplot as plt
import networkx as nx
import plotly.express as px
from sklearn import preprocessing
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


list_colors = px.colors.sequential.Plasma
IMAGE_PATH = []
TIME = ""


def set_time(time):
    global TIME
    TIME = time


def clear():
    global IMAGE_PATH
    IMAGE_PATH = []
    TIME = ""


def create_compare_fig():
    fig = plt.figure(figsize=(12, 12))
    for i in range(len(IMAGE_PATH)):
        ax = fig.add_subplot(2, 3, i+1)

        title = IMAGE_PATH[i].split("/")
        ax.set_title(title[2], fontsize=10)
        ax.axes.xaxis.set_visible(False)  # X軸を非表示に
        ax.axes.yaxis.set_visible(False)  # Y軸を非表示に

        img = mpimg.imread(IMAGE_PATH[i])
        plt.imshow(img)

        size = title[3].split("x")
    img_path = './result/compare/' + size[0] + TIME + '.png'
    plt.savefig(img_path)
    # plt.show()


def create_and_save_graph(graph, pos, node_color, edge_color, dir_name, width, height, name=None):
    G = nx.DiGraph()

    G.add_nodes_from(graph.nodes)
    G.add_edges_from(graph.edges)

    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G, pos, False,
                     node_color=node_color, edge_color=edge_color)

    img_path = './result/' + dir_name + '/' + \
        str(width) + 'x' + str(height) + '-' + TIME + '.png'
    plt.savefig(img_path)
    IMAGE_PATH.append(img_path)


def get_color(delta, node_len):
    delta01 = preprocessing.minmax_scale(delta).tolist()
    color = []
    for i in range(node_len):
        c_idx = int(delta01[i]*10)
        if c_idx >= len(list_colors):
            c_idx = len(list_colors)-1
        color.append(list_colors[c_idx])
    return color


def convert_graph_dict(nodes, pos):
    dict_pos = {}
    cnt = 0
    for node in nodes:
        dict_pos[node] = pos[cnt]
        cnt += 1
    return dict_pos


def draw_graph(graph, pos, delta, edge_score, node_len, dir_name, width, height):
    node_color = get_color(delta, node_len)
    edge_color = get_color(edge_score, node_len)
    # グラフ描画
    dict_pos = convert_graph_dict(graph.nodes, pos)
    create_and_save_graph(graph, dict_pos,  node_color, edge_color,
                          dir_name, width, height)
