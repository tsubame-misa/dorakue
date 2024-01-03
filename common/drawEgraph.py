
import matplotlib.pyplot as plt
import plotly.express as px
import os
import setup
import matplotlib.patches as pat
from matplotlib import collections
from common import calcDrawInfo, egraphCalcDrawInfo


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


def create_pos9(pos):
    add_len = [-1, 0, 1]
    pos9 = []
    for key in pos:
        for w in add_len:
            for h in add_len:
                x, y = pos[key]
                pos9.append([x+w, y+h])
    return pos9

def select_node(pos, u, v):
    _len = 1
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
            if _dist > adist:
                best_pos[0] = x
                best_pos[1] = y
                _dist = adist

    is_wrap = not(best_pos[0] == pos[v][0] and best_pos[1] == pos[v][1])

    return best_pos, is_wrap    

def draw_node(pos, ax):
    x = [p[0] for p in pos]
    y = [p[1] for p in pos]
    size = max(max(x)-min(x) ,max(y)-min(y))

    for p in pos:
        C = pat.Circle(xy=(p[0], p[1]), radius=1/(size*100), color=(0.3, 0.3, 0.3, 0.5))
        ax.add_patch(C)

def draw_edge(graph, pos, ax, debug=False):
    edge_lines = []
    wrap_lines = []
    wrap_lines2 = []

    for i, j in graph.edges:
        best_pos, is_wrap = select_node(pos, i, j)

        if is_wrap:
            line = [(pos[i][0], pos[i][1]),
                    (best_pos[0], best_pos[1])]
            if debug:
                wrap_lines.append(line)
            else:
                edge_lines.append(line)

            best_pos, is_wrap = select_node(pos,  j, i)
            line = [(pos[j][0], pos[j][1]),
                    (best_pos[0], best_pos[1])]
            if debug:
                wrap_lines2.append(line)
            else:
                edge_lines.append(line)
        else:
            line = [(pos[i][0], pos[i][1]),
                    (pos[j][0], pos[j][1])]
            edge_lines.append(line)

    if debug:
        line_collection = collections.LineCollection(
            edge_lines, color=("green",), linewidths=(0.5,))
    else:
        line_collection = collections.LineCollection(
            edge_lines, color=(0.3, 0.3, 0.3), linewidths=(0.5,))
    ax.add_collection(line_collection)

    line_collection = collections.LineCollection(
        wrap_lines, color=("red",), linewidths=(0.5,))
    ax.add_collection(line_collection)

    line_collection = collections.LineCollection(
        wrap_lines2, color=("orange",), linewidths=(0.5,))
    ax.add_collection(line_collection)    



def test(pos, graph):
    min_edge_len = float("inf")
    for p in pos:
        diff_x, diff_y, _pos = egraphCalcDrawInfo.shift_center(pos, p, 1, 1)
        max_edge_len = max(
            egraphCalcDrawInfo.dist_around(_pos, u, v) for u, v in graph.edges)
        if min_edge_len > max_edge_len:
            min_edge_len = max_edge_len
            center_idx = p

    diff_x, diff_y, fin_pos = egraphCalcDrawInfo.shift_center(pos, center_idx, 1, 1)

    return fin_pos


def tuple2array(pos):
    new_pos = {}
    for p in pos:
        new_pos[p] = [pos[p][0], pos[p][1]]
    return new_pos

def torus_graph_drawing(_pos, graph, name, multiple_num, time="xxx", debug=False):
    array_pos = tuple2array(_pos)
    pos = test(array_pos, graph)

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    ax.tick_params(labelbottom=False, labelleft=False,
                   labelright=False, labeltop=False, bottom=False, left=False, right=False, top=False)
    
    _len = 1

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

    pos9 = create_pos9(pos)
    draw_edge(graph, pos, ax, debug)
    draw_node(pos9, ax)

    dir_name = setup.get_dir_name()

    img_path = get_dir()+'/'+dir_name+'/torusSGD_wrap/' + \
        str(name) + '-' + str(multiple_num) + '-' + time + '.png'

    plt.savefig(img_path)
    IMAGE_PATH.append(img_path)

    plt.clf()
    plt.close()