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
中心に寄せてからのやつはやらない

"""

# 勾配ベクトルの一番長いもの(終了条件で使う予定だったけど使ってない)


def calc_delta(pos, Delta, k, l, node_len):
    max_delta = 0
    max_i = 0
    for i in range(node_len):
        # node[i]のストレスを出してるであってる？
        Ex = 0
        Ey = 0
        for j in range(node_len):
            if i == j:
                continue
            norm = math.sqrt((pos[i][0]-pos[j][0]) **
                             2 + (pos[i][1]-pos[j][1])**2)
            dx_ij = pos[i][0]-pos[j][0]
            dy_ij = pos[i][1]-pos[j][1]

            Ex += k[i][j]*dx_ij*(1.0-l[i][j]/norm)
            Ey += k[i][j]*dy_ij*(1.0-l[i][j]/norm)
        Delta[i] = math.sqrt(Ex*Ex+Ey*Ey)
        if Delta[i] > max_delta:
            max_delta = Delta[i]
            max_i = i
    return max_i


height = 800
width = 800
edge_len = 100

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
    d[x][y] = edge_len
    d[y][x] = edge_len

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

L0 = 1
L = L0/maxd
# 隣接行列の初期化
l = [[0]*node_len for i in range(node_len)]

K = 10
# 隣接行列の初期化
k = [[0]*node_len for i in range(node_len)]

for i in range(node_len):
    for j in range(node_len):
        if i == j:
            continue
        l[i][j] = d[i][j]
        k[i][j] = 1/(d[i][j]*d[i][j])


# posの初期化(ランダム)
pos = []
for i in range(node_len):
    x = L0*random.uniform(0, width)
    y = L0*random.uniform(0, height)
    pos.append([x, y])


Delta = [0]*node_len

max_i = calc_delta(pos, Delta, k, l, node_len)


for cnt1 in range(10):
    print(cnt1)
    # 全てのノードに対して中心に持ってきて動かす
    for max_i in range(node_len):
        for cnt2 in range(20):
            Exx = 0
            Exy = 0
            Eyy = 0
            Ex = 0
            Ey = 0

            for i in range(node_len):
                if i == max_i:
                    continue
                norm = math.sqrt((pos[max_i][0]-pos[i][0]) **
                                 2 + (pos[max_i][1]-pos[i][1])**2)
                dx_mi = pos[max_i][0]-pos[i][0]
                dy_mi = pos[max_i][1]-pos[i][1]

                Ex += k[max_i][i]*dx_mi*(1.0-l[max_i][i]/norm)
                Ey += k[max_i][i]*dy_mi*(1.0-l[max_i][i]/norm)

                Exy += k[max_i][i]*l[max_i][i]*dx_mi*dy_mi/(norm*norm*norm)
                Exx += k[max_i][i]*(1.0-l[max_i][i]*dy_mi *
                                    dy_mi/(norm*norm*norm))
                Eyy += k[max_i][i]*(1.0-l[max_i][i]*dx_mi *
                                    dx_mi/(norm*norm*norm))

            # ヘッセ行列=Exx*Eyy-Exy*Exy
            dx = Exx*Eyy-Exy*Exy
            dy = Exx*Eyy-Exy*Exy
            D = Exx*Eyy-Exy*Exy
            # 行列を計算すれば出てくる
            dx = - (Eyy*Ex-Exy*Ey)/D
            dy = -(-Exy*Ex+Exx*Ey)/D

            pos[max_i][0] += dx
            pos[max_i][1] += dy


pos0 = [(x, y) for x, y in pos]
center_idx = 0
min_edge_len = float("inf")
# 最適な中心を選ぶ
for i in range(node_len):
    diff_x = pos[i][0]-width/2
    diff_y = pos[i][1]-height/2

    def dist(u, v):
        dx = pos[u][0] - pos[v][0]
        dy = pos[u][1] - pos[v][1]
        return (dx ** 2 + dy ** 2) ** 0.5

    max_edge_len = max(dist(node2num[u], node2num[v]) for u, v in graph.edges)

    if min_edge_len > max_edge_len:
        min_edge_len = max_edge_len
        center_idx = i


calc_delta(pos, Delta, k, l, node_len)
delta01 = preprocessing.minmax_scale(Delta).tolist()
list_colors = px.colors.sequential.Plasma
node_color = []
print("delta01", delta01)
print(list_colors)
for i in range(node_len):
    c_idx = int(delta01[i]*10)
    print(c_idx)
    if c_idx >= len(list_colors):
        c_idx = len(list_colors)-1
    node_color.append(list_colors[c_idx])

print(center_idx)

dict_pos = {}
cnt = 0
for node in graph.nodes:
    dict_pos[node] = pos0[cnt]
    cnt += 1


G = nx.DiGraph()

G.add_nodes_from(graph.nodes)
G.add_edges_from(graph.edges)

plt.figure(figsize=(12, 12))
nx.draw_networkx(G, dict_pos, False, node_color=node_color)
plt.savefig('kame_result.png')
plt.show()
