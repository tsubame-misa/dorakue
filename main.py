import matplotlib.pyplot as plt
import networkx as nx
import json
import networkx as nx
from networkx.readwrite import json_graph
import glob
import random
import math


height = 1000
width = 1000

filename = './graph/les_miserables.json'
graph = json_graph.node_link_graph(json.load(open(filename)))

"""
それぞれのノードに対して、
1.中心に持ってくる

"""

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
    d[x][y] = 1
    d[y][x] = 1

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
        l[i][j] = L*d[i][j]
        k[i][j] = K/(d[i][j]*d[i][j])


# posの初期化(ランダム)
pos = []
for i in range(node_len):
    x = L0*random.uniform(0, width)
    y = L0*random.uniform(0, height)
    pos.append([x, y])


Delta = [0]*node_len


# この値一番ストレス(2点間の距離？)がでかいノードを調べてる？
def calc_delta():
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


max_i = calc_delta()

# print("delta", Delta)

# print("before pos", pos)
# print("max_i", max_i)

# 終了条件
cnt1 = 300
cnt2 = 300
print("delta", Delta[max_i])
pre_max_delta = Delta[max_i]+1
eps = 1.e-2

# 一番ストレスのでかいノードの位置を更新してストレスを下げてってる？
# ストレス計算するのに微分しないといけないのってなんで、今授業でやってるやつ？
while cnt1 > 0:
    cnt2 = 100
    while cnt2 > 0:
        Exx = 0
        Exy = 0
        Eyy = 0
        Ex = 0
        Ey = 0
        """
        ここで中心に持ってくる？
        max_iについて？
        """
        for i in range(node_len):
            if i == max_i:
                continue
            norm = math.sqrt((pos[max_i][0]-pos[i][0]) **
                             2 + (pos[max_i][1]-pos[i][1])**2)
            dx_mi = pos[max_i][0]-pos[i][0]
            dy_mi = pos[max_i][1]-pos[i][1]

            Ex += k[max_i][i]*l[max_i][i]*dx_mi*(1.0-d[max_i][i]/norm)
            Ey += k[max_i][i]*dy_mi*(1.0-d[max_i][i]/norm)

            Exy += k[max_i][i]*l[max_i][i]*dx_mi*dy_mi/(norm*norm*norm)
            Exx += k[max_i][i]*(1.0-dy_mi*dy_mi/(norm*norm*norm))
            Eyy += k[max_i][i]*(1.0-dx_mi*dx_mi/(norm*norm*norm))

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

        # ドラクエしないといけないのはこの部分であってる？
        pos[max_i][0] += dx
        pos[max_i][1] += dy

        Delta[max_i] = math.sqrt(Ex*Ex+Ey*Ey)
        cnt2 -= 1

    pre_max_delta = Delta[max_i]
    max_i = calc_delta()
    cnt1 -= 1
    # print("cnt2----------", max_i)
    print("delta", Delta[max_i], pre_max_delta, Delta[max_i] != pre_max_delta)

# print(pos)
print("delta", Delta[max_i])

# print(pos)

dict_pos = {}
cnt = 0
for node in graph.nodes:
    dict_pos[node] = pos[cnt]
    cnt += 1

G = nx.DiGraph()

G.add_nodes_from(graph.nodes)
G.add_edges_from(graph.edges)

nx.draw_networkx(G, dict_pos, False)
plt.show()

nx.draw_networkx(G)
plt.show()
