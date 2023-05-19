import matplotlib.pyplot as plt
import networkx as nx
import plotly.express as px
from sklearn import preprocessing
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json
import random


list_colors = px.colors.sequential.Plasma
image_path = []
log = dict()
pos = []


def add_log(key, value):
    log[key] = value


def get_time():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y%m%d%H%M%S')
    return d


def clear():
    images = []
    log = dict()
    pos = []


def create_compare_fig(time):
    fig = plt.figure(figsize=(12, 12))
    for i in range(len(image_path)):
        ax = fig.add_subplot(2, 3, i+1)

        title = image_path[i].split("/")
        ax.set_title(title[2], fontsize=10)
        ax.axes.xaxis.set_visible(False)  # X軸を非表示に
        ax.axes.yaxis.set_visible(False)  # Y軸を非表示に

        img = mpimg.imread(image_path[i])
        plt.imshow(img)

        size = title[3].split("x")
    img_path = './result/compare/' + size[0] + time + '.png'
    plt.savefig(img_path)
    plt.show()


def create_log(time):
    with open("./result/log/" + time + ".json", "w") as f:
        json.dump(log, f)


def create_and_save_graph(graph, pos, node_color, edge_color, dir_name, width, height, name=None):
    G = nx.DiGraph()

    G.add_nodes_from(graph.nodes)
    G.add_edges_from(graph.edges)

    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G, pos, False,
                     node_color=node_color, edge_color=edge_color)

    img_path = './result/' + dir_name + '/' + \
        str(width) + 'x' + str(height) + '-' + get_time() + '.png'
    plt.savefig(img_path)
    image_path.append(img_path)


def calc_mean(array):
    return sum(array)/len(array)


def calc_sd(array):
    mean = calc_mean(array)
    return sum((score - mean)**2 for score in array)/len(array)


def calc_evaluation_values(delta, dist_score):
    delta_mean = calc_mean(delta)
    delta_sd = calc_sd(delta)
    delta_sum = sum(delta)

    dist_mean = calc_mean(dist_score)
    dist_sd = calc_sd(dist_score)
    dist_sum = sum(dist_score)

    return {"delta": {"mean": delta_mean, "sd": delta_sd, "sum": delta_sum},
            "dist": {"mean": dist_mean, "sd": dist_sd, "sum": dist_sum}}


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


def dist_around(pos, u, v, width, height):
    dx = pos[u][0] - pos[v][0]
    dy = pos[u][1] - pos[v][1]
    dist = (dx ** 2 + dy ** 2) ** 0.5

    ax = pos[u][0] - ((pos[v][0]-(pos[u][0]-width/2) +
                       width) % width+(pos[u][0]-width/2))
    ay = pos[u][1] - ((pos[v][1]-(pos[u][1]-height/2) +
                       height) % height+(pos[u][1]-height/2))
    adist = (ax ** 2 + ay ** 2) ** 0.5
    return min(dist, adist)


def dist(pos, u, v):
    dx = pos[u][0] - pos[v][0]
    dy = pos[u][1] - pos[v][1]
    return (dx ** 2 + dy ** 2) ** 0.5


def draw_graph(graph, pos, delta, edge_score, node_len, dir_name, width, height):
    node_color = get_color(delta, node_len)
    edge_color = get_color(edge_score, node_len)
    # グラフ描画
    dict_pos = convert_graph_dict(graph.nodes, pos)
    create_and_save_graph(graph, dict_pos,  node_color, edge_color,
                          dir_name, width, height)


def init_pos(node_len, width, height):
    L0 = 1
    for i in range(node_len):
        x = L0*random.uniform(0, width)
        y = L0*random.uniform(0, height)
        pos.append([x, y])


def get_pos(node_len, width, height):
    if len(pos) == 0:
        init_pos(node_len, width, height)
    pos0 = [[x, y] for x, y in pos]
    return pos0
