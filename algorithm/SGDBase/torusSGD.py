import math
from common import calcDrawInfo, debug, initGraph, log, drawGraph
import setup
import itertools


def torus_sgd(graph, _width=None, _height=None):
    calcDrawInfo.clear_dorakue()
    loop = setup.get_SGD_loop()
    node_len = len(graph.nodes)
    node2num = initGraph.get_node2num_memoized(graph)

    # 最短経路
    d = initGraph.get_shortest_path(graph, node_len, node2num)
    # 重み
    w = [[1]*node_len for i in range(node_len)]
    # 重み(バネの強さ)
    k = [[0]*node_len for i in range(node_len)]
    # 理想的なバネの長さ(今回はL=1のため最短経路と一致)
    l = [[0]*node_len for i in range(node_len)]

    maxd = 0
    for i in range(node_len):
        for j in range(node_len):
            if maxd < d[i][j]:
                maxd = d[i][j]
            if i == j:
                continue
            w[i][j] = pow(d[i][j], -2)
            l[i][j] = d[i][j]
            k[i][j] = 1/(d[i][j]*d[i][j])

    height = maxd if _height == None else _height
    width = maxd if _width == None else _width
    pos = calcDrawInfo.get_pos(node_len, width, height)

    eps = 0.1
    eta_max = 1/(min(list(itertools.chain.from_iterable(w))))
    eta_min = eps/(max(list(itertools.chain.from_iterable(w))))
    eta = eta_max
    _lamda = -1*math.log(eta_min/eta_max)/loop

    for t in range(loop):
        pair_index = calcDrawInfo.get_random_pair(node_len, loop, t)
        eta = eta_max*pow(math.e, -1*_lamda*t)

        for i, j in pair_index:
            mu = w[i][j]*eta
            if mu > 1:
                mu = 1

            pos_ij = calcDrawInfo.dist_around_position(
                pos, i, j, width, height)

            rx = (calcDrawInfo.dist_around(pos, i, j, width, height)-d[i][j])/2 * (pos_ij[0]) / \
                calcDrawInfo.dist_around(pos, i, j, width, height)
            ry = (calcDrawInfo.dist_around(pos, i, j, width, height)-d[i][j])/2 * \
                (pos_ij[1]) / \
                calcDrawInfo.dist_around(pos, i, j, width, height)

            pos[i][0] = pos[i][0]-mu*rx
            pos[i][1] = pos[i][1]-mu*ry
            pos[j][0] = pos[j][0]+mu*rx
            pos[j][1] = pos[j][1]+mu*ry

            pos[i] = calcDrawInfo.dorakue(pos[i], width, height)
            pos[j] = calcDrawInfo.dorakue(pos[j], width, height)

    delta = calcDrawInfo.calc_delta_around(pos, k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                   calcDrawInfo.dist(pos, node2num[u], node2num[v]))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, pos, delta, edge_score,
                         node_len, "torusSGD", width, height)
    kame_log = log.calc_evaluation_values(delta, edge_score)

    log.add_log("torusSGD", kame_log)
    log.add_log("around", calcDrawInfo.get_has_dorakue())

    return kame_log["dist"]["sum"]
