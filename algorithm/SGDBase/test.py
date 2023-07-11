import math
from common import drawGraph
from common import log
from common import calcDrawInfo, debug
import setup
import itertools
import numpy as np
import networkx
from functools import lru_cache
import random


def sparse_sgd(graph, _width=None, _height=None):

    def get_radom_index():
        P = [i for i in range(h)]
        np.random.shuffle(P)
        P = P[:h+1]
        pair_index = set()
        for i, j in graph.edges:
            pair_index.add((node2num[i], node2num[j]))
        for i in range(node_len):
            for p in range(node_len):
                if i != p:
                    pair_index.add((i, p))

        pair_index = random.sample(pair_index, len(pair_index))
        return pair_index

    index = []
    height = 300 if _height == None else _height
    width = 300 if _width == None else _width
    edge_len = 100

    node_len = len(graph.nodes)
    h = node_len//5

    node2num = dict()
    cnt = 0
    for node in graph.nodes:
        node2num[node] = cnt
        cnt += 1

    P = [i for i in range(h)]
    np.random.shuffle(P)
    P = P[:h+1]
    # 隣接行列の初期化
    d = [[float('inf')]*node_len for i in range(node_len)]
    # w_ij=dij^(-2)
    wd = [[1]*node_len for i in range(node_len)]
    # 隣接行列の初期化
    l = [[0]*node_len for i in range(node_len)]

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
            if i < len(P):
                wd[P[i]][k] = 0

     # 隣接行列の初期化
    k = [[0]*node_len for i in range(node_len)]
    w = [[1]*node_len for i in range(node_len)]

    for i in range(node_len):
        for j in range(node_len):
            if d[i][j] != 0:
                w[i][j] = pow(d[i][j], -2)
            if i == j:
                continue
            l[i][j] = d[i][j]
            k[i][j] = 1/(d[i][j]*d[i][j])

    for i in range(node_len):
        for p in range(h):
            # if p が iの近傍じゃなかったら
            # s = len(d_pj < dpi) jはpに近い頂点セット
            s = 10
            wd[i][P[p]] = s*w[i][P[p]]

    for x_node, y_node in graph.edges:
        val = w[node2num[x_node]][node2num[y_node]]
        wd[node2num[x_node]][node2num[y_node]] = val
        wd[node2num[y_node]][node2num[x_node]] = val

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
            mu_i = min(w[i][j]*eta, 1)
            mu_j = min(w[j][i]*eta, 1)

            rx = (calcDrawInfo.dist_around(pos, i, j, width, height)-d[i][j])/2 * \
                (pos[i][0]-pos[j][0]) / \
                calcDrawInfo.dist_around(pos, i, j, width, height)
            ry = (calcDrawInfo.dist_around(pos, i, j, width, height)-d[i][j])/2 * \
                (pos[i][1]-pos[j][1]) / \
                calcDrawInfo.dist_around(pos, i, j, width, height)

            pos[i][0] = pos[i][0]-mu_i*rx
            pos[i][1] = pos[i][1]-mu_i*ry
            pos[j][0] = pos[j][0]+mu_j*rx
            pos[j][1] = pos[j][1]+mu_j*ry

    delta = calcDrawInfo.calc_delta_around(pos, k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                  calcDrawInfo.dist_around(pos, node2num[u], node2num[v], width, height))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, pos, delta, edge_score,
                         node_len, "sparseTorusSGD", width, height)
    kame_log = log.calc_evaluation_values(delta, edge_score)

    debug.add_node_a(pos)
    debug.add_index_a(index)

    log.add_log("sparseTorusSGD", kame_log)

    return kame_log["dist"]["sum"]
