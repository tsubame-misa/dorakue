import matplotlib.pyplot as plt
import networkx as nx
import json
import networkx as nx
from networkx.readwrite import json_graph
import glob
import random
import math

# この値一番ストレス(2点間の距離？)がでかいノードを調べてる？
# 勾配ベクトルの一番長いもの


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


def shift_center(pos, max_i, node_len):
    diff_x = pos[max_i][0]-width/2
    diff_y = pos[max_i][1]-height/2
    # ここをドラクエにする
    for i in range(node_len):
        pos[i][0] -= diff_x
        pos[i][1] -= diff_y

        # if pos[i][0] < 0 or pos[i][0] > width or pos[i][1] < 0 or pos[i][1] > height:
        #     print("to center", pos[i])

        if pos[i][0] < 0:
            pos[i][0] = width+pos[i][0]
        elif pos[i][0] > width:
            pos[i][0] = pos[i][0]-width

        if pos[i][1] < 0:
            pos[i][1] = height+pos[i][1]
        elif pos[i][1] > height:
            pos[i][1] = pos[i][1]-height
    return pos


def shift_flat(pos, diff_x, diff_y, node_len):
    for i in range(node_len):
        pos[i][0] += diff_x
        pos[i][1] += diff_y

        # if pos[i][0] < 0 or pos[i][0] > width or pos[i][1] < 0 or pos[i][1] > height:
        #     print("replace", pos[i])

        if pos[i][0] < 0:
            pos[i][0] = width+pos[i][0]
        elif pos[i][0] > width:
            pos[i][0] = pos[i][0]-width

        if pos[i][1] < 0:
            pos[i][1] = height+pos[i][1]
        elif pos[i][1] > height:
            pos[i][1] = pos[i][1]-height
    return pos


height = 500
width = 500

filename = './graph/les_miserables.json'
graph = json_graph.node_link_graph(json.load(open(filename)))


print(graph)
# ノードの一覧
print(graph.nodes)
# エッジの一覧
print(graph.edges)

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


# 終了条件
cnt1 = 50
while cnt1 > 0:
    print(cnt1)
    # 全てのノードに対して中心に持ってきて動かす
    for max_i in range(node_len):
        cnt2 = 20
        while cnt2 > 0:
            Exx = 0
            Exy = 0
            Eyy = 0
            Ex = 0
            Ey = 0
            # print(max_i)
            # max_iを中心に持ってくる
            diff_x = pos[max_i][0]-width/2
            diff_y = pos[max_i][1]-height/2
            pos = shift_center(pos, max_i, node_len)
            #
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
            # これがわからん
            dx = - (Eyy*Ex-Exy*Ey)/D
            dy = -(-Exy*Ex+Exx*Ey)/D

            """
            中心にずらした分をともとに戻す必要ってある？
            """

            # ドラクエしないといけないその2?
            pos[max_i][0] += dx
            pos[max_i][1] += dy

            # if pos[i][0] < 0 or pos[i][0] > width or pos[i][1] < 0 or pos[i][1] > height:
            #     print("add pos", pos[i])

            if pos[max_i][0] < 0:
                pos[max_i][0] = width+pos[max_i][0]
            elif pos[max_i][0] > width:
                pos[max_i][0] = pos[max_i][0]-width

            if pos[max_i][1] < 0:
                pos[max_i][1] = height+pos[max_i][1]
            elif pos[max_i][1] > height:
                pos[max_i][1] = pos[max_i][1]-height

            pos = shift_flat(pos, diff_x, diff_y, node_len)

            Delta[max_i] = math.sqrt(Ex*Ex+Ey*Ey)
            cnt2 -= 1
    cnt1 -= 1

pos0 = [(x, y) for x, y in pos]
m_pos = pos
center_idx = 0
min_edge_len = float("inf")
# 最適な中心を選ぶ
for i in range(node_len):
    diff_x = pos[i][0]-width/2
    diff_y = pos[i][1]-height/2
    m_pos = shift_center(m_pos, i, node_len)

    def dist(u, v):
        dx = pos[u][0] - pos[v][0]
        dy = pos[u][1] - pos[v][1]
        return (dx ** 2 + dy ** 2) ** 0.5
    max_edge_len = max(dist(node2num[u], node2num[v]) for u, v in graph.edges)
    # max_edge_len = 0
    # for j in range(node_len):
    #     edge_len = math.sqrt((pos[i][0]-pos[j][0]) **
    #                          2 + (pos[i][1]-pos[j][1])**2)
    #     if max_edge_len < edge_len:
    #         max_edge_len = edge_len
    if min_edge_len > max_edge_len:
        min_edge_len = max_edge_len
        center_idx = i

    m_pos = shift_flat(m_pos, diff_x, diff_y, node_len)

fin_pos = shift_center(pos, center_idx, node_len)

print(center_idx)

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

G = nx.DiGraph()

G.add_nodes_from(graph.nodes)
G.add_edges_from(graph.edges)

plt.figure(figsize=(12, 12))
nx.draw_networkx(G, dict_pos, False)
plt.savefig('result.png')
plt.show()

plt.figure(figsize=(12, 12))
nx.draw_networkx(G, fin_dict_pos, False)
plt.savefig('result2.png')
plt.show()

# nx.draw_networkx(G, fin_dict_pos, False)
# plt.show()

# nx.draw_networkx(G)
# plt.show()
