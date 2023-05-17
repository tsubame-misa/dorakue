import matplotlib.pyplot as plt
import networkx as nx
import json
import networkx as nx
from networkx.readwrite import json_graph
import glob
import random
import math
import plotly.express as px
from sklearn import preprocessing


"""
K, Lを除いた版も試してみる？
"""
# 理想の長さと実際の長さ  sum(d[u][v]-dist(u, v) )**2


def dist(pos, u, v):
    dx = pos[u][0] - pos[v][0]
    dy = pos[u][1] - pos[v][1]
    return (dx ** 2 + dy ** 2) ** 0.5


def calc_delta(pos, node_len):
    Delta = [0]*node_len
    for i in range(node_len):
        Ex = 0
        Ey = 0
        diff_x, diff_y, pos = shift_center(pos, i, node_len)
        for j in range(node_len):
            if i == j:
                continue
            norm = math.sqrt((pos[i][0]-pos[j][0]) **
                             2 + (pos[i][1]-pos[j][1])**2)
            dx_ij = pos[i][0]-pos[j][0]
            dy_ij = pos[i][1]-pos[j][1]

            Ex += dx_ij*(1.0-d[i][j]/norm)
            Ey += dy_ij*(1.0-d[i][j]/norm)
        Delta[i] = math.sqrt(Ex*Ex+Ey*Ey)
        pos = shift_flat(pos, diff_x, diff_y, node_len)

    return Delta


def dorakue(pos):
    if pos[0] < 0:
        pos[0] = width+pos[0]
    elif pos[0] > width:
        pos[0] = pos[0]-width

    if pos[1] < 0:
        pos[1] = height+pos[1]
    elif pos[1] > height:
        pos[1] = pos[1]-height

    return pos


def shift_center(pos, idx, node_len):
    diff_x = pos[idx][0]-width/2
    diff_y = pos[idx][1]-height/2

    for i in range(node_len):
        pos[i][0] -= diff_x
        pos[i][1] -= diff_y
        pos[i] = dorakue(pos[i])

    return diff_x, diff_y, pos


def shift_flat(pos, diff_x, diff_y, node_len):
    for i in range(node_len):
        pos[i][0] += diff_x
        pos[i][1] += diff_y

        pos[i] = dorakue(pos[i])

    return pos


filename = './graph/les_miserables.json'
graph = json_graph.node_link_graph(json.load(open(filename)))

node_len = len(graph.nodes)

node2num = dict()
cnt = 0
for node in graph.nodes:
    node2num[node] = cnt
    cnt += 1

# 隣接行列の初期化
d = [[float('inf')]*node_len for i in range(node_len)]
# 隣接行列の作成
for i in range(node_len):
    d[i][i] = 0
for x_node, y_node in graph.edges:
    # 重みがないので1
    x = node2num[x_node]
    y = node2num[y_node]
    d[x][y] = 100
    d[y][x] = 100

# ワーシャルフロイド(最短経路)
for k in range(node_len):
    for i in range(node_len):
        for j in range(node_len):
            d[i][j] = min(d[i][j], d[i][k]+d[k][j])

maxd = 0
mind = float("inf")
for i in range(node_len):
    for j in range(i, node_len):
        if maxd < d[i][j]:
            maxd = d[i][j]

height = maxd
width = maxd

print("width,height", width)

# posの初期化(ランダム)
pos = []
for i in range(node_len):
    x = random.uniform(0, width)
    y = random.uniform(0, height)
    pos.append([x, y])


for cnt1 in range(50):
    print(cnt1)
    # 全てのノードに対して中心に持ってきて動かす
    for max_i in range(node_len):
        for cnt2 in range(20):
            Exx = 0
            Exy = 0
            Eyy = 0
            Ex = 0
            Ey = 0

            diff_x, diff_y, pos = shift_center(pos, max_i, node_len)

            for i in range(node_len):
                if i == max_i:
                    continue
                norm = math.sqrt((pos[max_i][0]-pos[i][0]) **
                                 2 + (pos[max_i][1]-pos[i][1])**2)
                dx_mi = pos[max_i][0]-pos[i][0]
                dy_mi = pos[max_i][1]-pos[i][1]

                Ex += dx_mi*(1.0-d[max_i][i]/norm)
                Ey += dy_mi*(1.0-d[max_i][i]/norm)

                Exy += dx_mi*dy_mi/(norm*norm*norm)
                Exx += (1.0-d[max_i][i]*dy_mi *
                        dy_mi/(norm*norm*norm))
                Eyy += (1.0-d[max_i][i]*dx_mi *
                        dx_mi/(norm*norm*norm))

            # ヘッセ行列=Exx*Eyy-Exy*Exy
            dx = Exx*Eyy-Exy*Exy
            dy = Exx*Eyy-Exy*Exy
            D = Exx*Eyy-Exy*Exy
            # 行列計算
            dx = - (Eyy*Ex-Exy*Ey)/D
            dy = -(-Exy*Ex+Exx*Ey)/D

            pos[max_i][0] += dx
            pos[max_i][1] += dy
            pos[max_i] = dorakue(pos[max_i])

            pos = shift_flat(pos, diff_x, diff_y, node_len)

pos0 = [(x, y) for x, y in pos]

center_idx = 0
min_edge_len = float("inf")
# 最適な中心を選ぶ
for i in range(node_len):
    diff_x, diff_y, pos = shift_center(pos, i, node_len)
    max_edge_len = max(
        dist(pos, node2num[u], node2num[v]) for u, v in graph.edges)
    if min_edge_len > max_edge_len:
        min_edge_len = max_edge_len
        center_idx = i

    pos = shift_flat(pos, diff_x, diff_y, node_len)

diff_x, diff_y, fin_pos = shift_center(pos, center_idx, node_len)

delta = calc_delta(pos, node_len)
delta01 = preprocessing.minmax_scale(delta).tolist()
list_colors = px.colors.sequential.Plasma
node_color = []
for i in range(node_len):
    c_idx = int(delta01[i]*10)
    if c_idx >= len(list_colors):
        c_idx = len(list_colors)-1
    node_color.append(list_colors[c_idx])

dict_pos = {}
cnt = 0
for node in graph.nodes:
    dict_pos[node] = pos0[cnt]
    cnt += 1

fin_dict_pos = {}
cnt = 0
for node in graph.nodes:
    fin_dict_pos[node] = fin_pos[cnt]
    cnt += 1

dist_score = sum(((d[node2num[u]][node2num[v]] -
                 dist(pos, node2num[u], node2num[v]))**2 for u, v in graph.edges))


print(dist_score)

G = nx.DiGraph()

G.add_nodes_from(graph.nodes)
G.add_edges_from(graph.edges)

plt.figure(figsize=(12, 12))
nx.draw_networkx(G, fin_dict_pos, False, node_color=node_color)
plt.savefig('result2.png')
plt.show()
