import math
from common import drawGraph
from common import log
from common import calcDrawInfo, debug
import setup
import itertools
import numpy as np
from functools import lru_cache
import random


def dijkstra(graph, start):
    # 初期化
    n = len(graph)
    visited = [False] * n
    distance = [float("inf")] * n
    distance[start] = 0

    # ダイクストラ法
    for i in range(n):
        # 未処理の中で最小の距離を持つ頂点を探す
        min_distance = float("inf")
        for j in range(n):
            if not visited[j] and distance[j] < min_distance:
                min_distance = distance[j]
                u = j

        # 訪問済みにする
        visited[u] = True

        # uから到達可能な頂点の距離を更新する
        for v in range(n):
            if not visited[v] and graph[u][v] != 0:
                new_distance = distance[u] + graph[u][v]
                if new_distance < distance[v]:
                    distance[v] = new_distance
    return distance


def sparse_sgd(graph, _width=None, _height=None):

    def get_radom_index():
        pair_index = set()
        for i, j in graph.edges:
            pair_index.add((node2num[i], node2num[j]))
        for i in range(node_len):
            for p in P:
                if i != p:
                    # ここ逆にするとバグる
                    pair_index.add((p, i))
        pair_index = random.sample(pair_index, len(pair_index))
        return pair_index

    index = []
    height = 300 if _height == None else _height
    width = 300 if _width == None else _width
    edge_len = 100

    node_len = len(graph.nodes)
    h = node_len//3

    print(h)

    node2num = dict()
    cnt = 0
    for node in graph.nodes:
        node2num[node] = cnt
        cnt += 1

    # 隣接行列の初期化
    d = [[float('inf')]*node_len for i in range(node_len)]
    # w_ij=dij^(-2)
    wd = [[1]*node_len for i in range(node_len)]
    # 隣接行列の初期化
    l = [[0]*node_len for i in range(node_len)]

    # 隣接行列の作成
    for i in range(node_len):
        # d[i][i] = 0
        l[i][i] = 0
    for x_node, y_node in graph.edges:
        # 重みがないので1
        x = node2num[x_node]
        y = node2num[y_node]
        # d[x][y] = edge_len
        # d[y][x] = edge_len
        l[x][y] = edge_len
        l[y][x] = edge_len

    # # これまでに選択されたピボットへの最大最短パスを持つ頂点
    P = []
    # pivot = random.randint(0, node_len-1)
    pivot = 0
    P.append(pivot)
    for i in range(h-1):
        d[pivot] = dijkstra(l, pivot)
        d_sum = []
        d_cumulative_sum = [0]
        for k in range(node_len):
            if k in P:
                d_sum.append(0)
                d_cumulative_sum.append(d_cumulative_sum[k])
                continue
            _d = 0
            for p in P:
                if d[p][k] != float("inf"):
                    _d += d[p][k]
            d_sum.append(_d)
            d_cumulative_sum.append(d_cumulative_sum[k]+_d)
        # 最大値を取るやつ
        # pivot = d_sum.index(max(d_sum))
        # 確率のやつ？？
        p = random.randint(0, d_cumulative_sum[-1])
        for v in range(len(d_cumulative_sum)-1):
            if d_cumulative_sum[v] < p and p <= d_cumulative_sum[v+1]:
                pivot = v
        P.append(pivot)
    print(P)

    # これまでに選択されたピボットへの最大最短パスを持つ頂点
    # P = []
    # pivot = random.randint(0, node_len-1)
    # P.append(pivot)
    # while len(P) < h:
    #     _d = dijkstra(l, pivot)
    #     pivot = _d.index(max(_d))
    #     while pivot in P:
    #         _d[pivot] = 0
    #         pivot = _d.index(max(_d))
    #         print(pivot)
    #     P.append(pivot)
    # print(P)

    # ワーシャルフロイド(最短経路)
    # for k in range(node_len):
    #     for i in range(node_len):
    #         for j in range(node_len):
    #             d[i][j] = min(d[i][j], d[i][k]+d[k][j])
    #         if i < len(P):
    #             wd[P[i]][k] = 0
    for p in P:
        d[p] = dijkstra(l, p)
        wd[p] = [0]*node_len

    # 隣接行列の初期化
    k = [[0]*node_len for i in range(node_len)]
    w = [[1]*node_len for i in range(node_len)]

    for i in range(node_len):
        for j in P:
            if d[j][i] != 0:
                w[j][i] = pow(d[j][i], -2)
                wd[j][i] = pow(d[j][i], -2)
                # ないけどこれいるはず

                # print("###", w[j][i])

    for i in range(node_len):
        for p in P:
            near_i = [i for i, x in enumerate(l[i]) if x <= 100]
            near_p = [i for i, x in enumerate(l[p]) if x <= 100]
            # pがiの近傍じゃなかったら
            if not p in near_i:
                # s = len(d_pj < dpi) jはpに近い頂点セット
                cnt = 0
                for j in near_p:
                    if d[p][j] < d[i][p]:
                        cnt += 1
                d[i] = dijkstra(l, i)
                w[i][p] = pow(d[i][p], -2)
                wd[i][p] = cnt*w[i][p]

    for x_node, y_node in graph.edges:
        i = node2num[x_node]
        j = node2num[y_node]
        d[i] = dijkstra(l, node2num[x_node])
        # val = w[i][j]
        val = pow(d[i][j], -2)
        wd[i][j] = w[i][j]
        wd[j][i] = w[i][j]
        k[i][j] = 1 / (d[i][j] * d[i][j])

    pos = calcDrawInfo.get_pos(node_len, width, height)

    loop1, loop2 = setup.get_loop()

    # loop=100くらいがちょうど良さそう
    eps = 0.1
    eta_max = 1/(min(list(itertools.chain.from_iterable(w))))
    eta_min = eps/(max(list(itertools.chain.from_iterable(w))))
    eta = eta_max
    _lamda = -1*math.log(eta_min/eta_max)/loop1

    debug.add_node_a(pos)

    print(pos[0])

    for t in range(loop1):
        pair_index = get_radom_index()
        eta = eta_max*pow(math.e, -1*_lamda*t)
        for i, j in pair_index:
            index.append([i, j])
            # print(wd[i][j], wd[j][i])
            # print(w[i][j], w[j][i], wd[i][j], wd[j][i], i in P, j in P)
            mu_i = min(w[i][j]*eta, 1)
            mu_j = min(w[j][i]*eta, 1)

            rx = (calcDrawInfo.dist(pos, i, j)-d[i][j])/2 * \
                (pos[i][0]-pos[j][0])/calcDrawInfo.dist(pos, i, j)
            ry = (calcDrawInfo.dist(pos, i, j)-d[i][j])/2 * \
                (pos[i][1]-pos[j][1])/calcDrawInfo.dist(pos, i, j)

            pos[i][0] = pos[i][0]-mu_i*rx
            pos[i][1] = pos[i][1]-mu_i*ry
            pos[j][0] = pos[j][0]+mu_j*rx
            pos[j][1] = pos[j][1]+mu_j*ry

    delta = calcDrawInfo.calc_delta(pos, k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                  calcDrawInfo.dist(pos, node2num[u], node2num[v]))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, pos, delta, edge_score,
                         node_len, "sparseSGD", width, height)
    kame_log = log.calc_evaluation_values(delta, edge_score)

    debug.add_node_a(pos)
    debug.add_index_a(index)

    log.add_log("sparseSGD", kame_log)

    return kame_log["dist"]["sum"]
