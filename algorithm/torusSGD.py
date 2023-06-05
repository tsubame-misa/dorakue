import math
from common import drawGraph
from common import log
from common import calcDrawInfo
import setup
import random
import itertools
import numpy as np


def torus_sgd(graph, _width=None, _height=None):
    index = []

    def calc_delta(pos,  k, l, node_len, width, height):
        Delta = [0]*node_len
        max_delta = 0
        max_i = 0
        for i in range(node_len):
            Ex = 0
            Ey = 0
            _pos = [[x, y] for x, y in pos]
            diff_x, diff_y, _pos = calcDrawInfo.shift_center(
                _pos, i, node_len, width, height)
            for j in range(node_len):
                if i == j:
                    continue
                norm = math.sqrt((_pos[i][0]-_pos[j][0]) **
                                 2 + (_pos[i][1]-_pos[j][1])**2)
                dx_ij = _pos[i][0]-_pos[j][0]
                dy_ij = _pos[i][1]-_pos[j][1]

                Ex += k[i][j]*dx_ij*(1.0-l[i][j]/norm)
                Ey += k[i][j]*dy_ij*(1.0-l[i][j]/norm)
            Delta[i] = math.sqrt(Ex*Ex+Ey*Ey)
            if Delta[i] > max_delta:
                max_delta = Delta[i]
                max_i = i

        return max_i

    edge_len = 100

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

    # w_ij=dij^(-2)
    w = [[float('inf')]*node_len for i in range(node_len)]
    for i in range(node_len):
        for j in range(node_len):
            if d[i][j] != 0:
                w[i][j] = pow(d[i][j], -2)

    maxd = 0
    for i in range(node_len):
        for j in range(i, node_len):
            if maxd < d[i][j]:
                maxd = d[i][j]

    height = maxd if _height == None else _height
    width = maxd if _width == None else _width

    # 隣接行列の初期化
    l = [[0]*node_len for i in range(node_len)]

    # 隣接行列の初期化
    k = [[0]*node_len for i in range(node_len)]

    for i in range(node_len):
        for j in range(node_len):
            if i == j:
                continue
            l[i][j] = d[i][j]
            k[i][j] = 1/(d[i][j]*d[i][j])

    pos = calcDrawInfo.get_pos(node_len, width, height)

    max_i = calc_delta(pos, k, l, node_len, width, height)

    loop1, loop2 = setup.get_loop()

    # TODO:etaの初期値と更新周りの調整
    eta = 2
    for cnt1 in range(loop1):
        pare_index = [list(p) for p in itertools.combinations(
            [i for i in range(node_len)], 2)]
        np.random.shuffle(pare_index)
        eta *= 0.95
        # print(eta)
        for i, j in pare_index:
            # mu = w[i][j]*eta
            mu = eta
            if mu > 1:
                mu = 1
            pos_ij = calcDrawInfo.dorakue(
                [pos[i][0]-pos[j][0], pos[i][1]-pos[j][1]], width, height)
            # pos_ij = [pos[i][0]-pos[j][0], pos[i][1]-pos[j][1]]
            # print([pos[i][0]-pos[j][0], pos[i][1]-pos[j][1]])
            # print(pos_ij)
            # print("--------------")
            rx = (calcDrawInfo.dist_around(pos, i, j, width, height)-d[i][j])/2 * \
                (pos_ij[0]) / \
                calcDrawInfo.dist_around(pos, i, j, width, height)
            ry = (calcDrawInfo.dist_around(pos, i, j, width, height)-d[i][j])/2 * \
                (pos_ij[1]) / \
                calcDrawInfo.dist_around(pos, i, j, width, height)
            pos[i][0] = pos[i][0]-mu*rx
            pos[i][1] = pos[i][1]-mu*ry
            pos[j][0] = pos[j][0]+mu*rx
            pos[j][1] = pos[j][1]+mu*ry

    delta = calcDrawInfo.calc_delta(pos, k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                   calcDrawInfo.dist(pos, node2num[u], node2num[v]))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, pos, delta, edge_score,
                         node_len, "torusSGD", width, height)
    kame_log = log.calc_evaluation_values(delta, edge_score)

    calcDrawInfo.add_node_a(pos)
    calcDrawInfo.add_index_a(index)

    log.add_log("torusSGD", kame_log)

    return kame_log["dist"]["sum"]
