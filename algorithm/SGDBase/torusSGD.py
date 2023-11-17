import math
from common import calcDrawInfo, debug, initGraph, log, drawGraph, aestheticsMeasures
import setup
import itertools


def torus_sgd(graph, file_name, _width=None, _height=None):
    calcDrawInfo.clear_dorakue()
    loop = setup.get_SGD_loop()
    node_len = len(graph.nodes)
    node2num = initGraph.get_node2num_memoized(graph)

    # 最短経路
    d = initGraph.get_shortest_path(graph, node_len, node2num, file_name)
    # 重み
    w = [[1]*node_len for i in range(node_len)]
    # 重み(バネの強さ)
    k = [[0]*node_len for i in range(node_len)]
    # 理想的なバネの長さ(今回はL=1のため最短経路と一致)
    l = [[0]*node_len for i in range(node_len)]

    maxd = initGraph.get_maxd(graph, file_name)
    for _i in graph.nodes:
        for _j in graph.nodes:
            i = node2num[str(_i)]
            j = node2num[str(_j)]
            if i == j:
                continue
            w[i][j] = pow(d[_i][_j], -2)
            l[i][j] = d[_i][_j]
            k[i][j] = 1/(d[_i][_j]*d[_i][_j])

    height = maxd if _height == None else _height
    width = maxd if _width == None else _width
    pos = initGraph.get_pos(node_len, width, height)

    eps = 0.1
    eta_max = 1/(min(list(itertools.chain.from_iterable(w))))
    eta_min = eps/(max(list(itertools.chain.from_iterable(w))))
    eta = eta_max
    _lamda = -1*math.log(eta_min/eta_max)/loop

    for t in range(loop):
        pair_index = initGraph.get_random_pair(graph, loop, t)

        eta = eta_max*pow(math.e, -1*_lamda*t)

        for _i, _j in pair_index:

            i = node2num[str(_i)]
            j = node2num[str(_j)]
            mu = w[i][j]*eta
            if mu > 1:
                mu = 1

            pos_ij = calcDrawInfo.dist_around_position(
                pos, i, j, width, height, l[i][j])

            if i == j:
                rx = 0
                ry = 0
            else:
                rx = (calcDrawInfo.dist_around(pos, i, j, width, height, l[i][j])-d[_i][_j])/2 * (pos_ij[0]) / \
                    calcDrawInfo.dist_around(pos, i, j, width, height, l[i][j])
                ry = (calcDrawInfo.dist_around(pos, i, j, width, height, l[i][j])-d[_i][_j])/2 * \
                    (pos_ij[1]) / \
                    calcDrawInfo.dist_around(pos, i, j, width, height, l[i][j])

            pos[i][0] = pos[i][0]-mu*rx
            pos[i][1] = pos[i][1]-mu*ry
            pos[j][0] = pos[j][0]+mu*rx
            pos[j][1] = pos[j][1]+mu*ry

            pos[i] = calcDrawInfo.dorakue(pos[i], width, height)
            pos[j] = calcDrawInfo.dorakue(pos[j], width, height)

    pos0 = [[x, y] for x, y in pos]

    isWrap = calcDrawInfo.get_has_dorakue()

    center_idx = 0
    min_edge_len = float("inf")
    # 最適な中心を選ぶ
    for i in range(node_len):
        diff_x, diff_y, _pos = calcDrawInfo.shift_center(
            pos0, i, node_len, width, height)
        max_edge_len = max(
            calcDrawInfo.dist(_pos, node2num[str(u)], node2num[str(v)]) for u, v in graph.edges)
        if min_edge_len > max_edge_len:
            min_edge_len = max_edge_len
            center_idx = i

    diff_x, diff_y, fin_pos = calcDrawInfo.shift_center(
        pos, center_idx, node_len, width, height)

    delta = calcDrawInfo.calc_delta_around(
        fin_pos, k, l, node_len, width, height)
    edge_score = [(d[u][v] -
                   calcDrawInfo.dist_around(fin_pos, node2num[str(u)], node2num[str(v)], width, height, l[node2num[str(u)]][node2num[str(v)]]))**2 for u, v in graph.edges]
    # delta = calcDrawInfo.calc_delta(
    #     fin_pos, k, l, node_len)
    # edge_score = [(d[node2num[str(u)]][node2num[str(v)]] -
    #                calcDrawInfo.dist(fin_pos, node2num[str(u)], node2num[str(v)]))**2 for u, v in graph.edges]

    drawGraph.draw_graph(graph, fin_pos, delta, edge_score,
                         node_len, "torusSGD", width, height, file_name)
    drawGraph.torus_graph_drawing(
        pos, l, node2num, graph, width, "torusSGD_wrap", file_name)
    # kame_log = aestheticsMeasures.calc_evaluation_values(
    #     delta, edge_score, graph, node2num, fin_pos, l, width, height,  calcDrawInfo.get_has_dorakue())
    kame_log = aestheticsMeasures.calc_torus_evaluation_values(
        delta, edge_score, graph, node2num, pos, l, float(width), maxd, d)

    kame_log["wrap"] = isWrap
    kame_log["pos"] = fin_pos
    kame_log["k"] = k
    kame_log["l"] = l
    kame_log["d"] = d
    kame_log["node2num"] = node2num
    kame_log["node_len"] = node_len
    log.add_log("torusSGD", kame_log)
    debug.add_node_b(fin_pos)

    return kame_log["dist"]["sum"]
