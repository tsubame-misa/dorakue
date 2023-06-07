import math
from common import drawGraph
from common import log
from common import calcDrawInfo
import setup


def torus_center(graph, _width=None, _height=None):
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
    for i in range(node_len):
        for j in range(i, node_len):
            if maxd < d[i][j]:
                maxd = d[i][j]

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

    height = maxd if _height == None else _height
    width = maxd if _width == None else _width

    pos = calcDrawInfo.get_pos(node_len, width, height)

    loop1, loop2 = setup.get_loop()

    for cnt1 in range(loop1):
        for max_i in range(node_len):
            for cnt2 in range(loop2):
                Exx = 0
                Exy = 0
                Eyy = 0
                Ex = 0
                Ey = 0

                diff_x, diff_y, pos = calcDrawInfo.shift_center(
                    pos, max_i, node_len, width, height)

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
                # 行列計算
                dx = - (Eyy*Ex-Exy*Ey)/D
                dy = -(-Exy*Ex+Exx*Ey)/D

                pos[max_i][0] += dx
                pos[max_i][1] += dy
                pos[max_i] = calcDrawInfo.dorakue(
                    pos[max_i], width, height)

                pos = calcDrawInfo.shift_flat(
                    pos, diff_x, diff_y, node_len, width, height)

    pos0 = [[x, y] for x, y in pos]

    center_idx = 0
    min_edge_len = float("inf")
    # 最適な中心を選ぶ
    for i in range(node_len):
        diff_x, diff_y, pos = calcDrawInfo.shift_center(
            pos, i, node_len, width, height)
        max_edge_len = max(
            calcDrawInfo.dist(pos, node2num[u], node2num[v]) for u, v in graph.edges)
        if min_edge_len > max_edge_len:
            min_edge_len = max_edge_len
            center_idx = i
        pos = calcDrawInfo.shift_flat(
            pos, diff_x, diff_y, node_len, width, height)

    diff_x, diff_y, fin_pos = calcDrawInfo.shift_center(
        pos0, center_idx, node_len, width, height)

    pos0 = [[x, y] for x, y in fin_pos]
    pos1 = [[x, y] for x, y in fin_pos]

    delta = calcDrawInfo.calc_delta_around(
        pos0,  k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                   calcDrawInfo.dist_around(fin_pos, node2num[u], node2num[v], width, height))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, fin_pos, delta, edge_score,
                         node_len, "dorakue_center_around", width, height)
    center_around_log = log.calc_evaluation_values(delta, edge_score)

    delta = calcDrawInfo.calc_delta(pos1,  k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                   calcDrawInfo.dist(fin_pos, node2num[u], node2num[v]))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, fin_pos, delta, edge_score,
                         node_len, "dorakue_center", width, height)
    center_log = log.calc_evaluation_values(delta, edge_score)

    log.add_log("dorakue_log", center_log)
    log.add_log("dorakue_around", center_around_log)

    return min(center_log["dist"]["sum"], center_around_log["dist"]["sum"])
