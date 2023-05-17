import matplotlib.pyplot as plt
import networkx as nx
import plotly.express as px
from sklearn import preprocessing
import datetime

list_colors = px.colors.sequential.Plasma


def create_and_save_graph(graph, pos, node_color, edge_color, dir_name):
    G = nx.DiGraph()

    G.add_nodes_from(graph.nodes)
    G.add_edges_from(graph.edges)

    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y%m%d%H%M%S')

    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G, pos, False,
                     node_color=node_color, edge_color=edge_color)
    plt.savefig('./result/' + dir_name + '/' + d + '.png')


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

    ax = (pos[v][0]-(pos[u][0]-width/2) +
          width) % width+(pos[u][0]-width/2)
    ay = (pos[v][1]-(pos[u][1]-height/2) +
          height) % height+(pos[u][1]-height/2)
    adist = (ax ** 2 + ay ** 2) ** 0.5
    return min(dist, adist)
