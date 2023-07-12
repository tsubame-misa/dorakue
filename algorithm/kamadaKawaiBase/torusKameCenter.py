import math
from common import calcDrawInfo, aestheticsMeasures, log, drawGraph
import setup
from common import initGraph


def torus_kame(graph, file_name, _width=None, _height=None):
    calcDrawInfo.clear_dorakue()
    loop1, loop2 = setup.get_loop()
    node_len = len(graph.nodes)
    node2num = initGraph.get_node2num_memoized(graph)

    # 最短経路
    d = initGraph.get_shortest_path(graph, node_len, node2num, file_name)
    # 重み(バネの強さ)
    k = [[0]*node_len for i in range(node_len)]
    # 理想的なバネの長さ(今回はL=1のため最短経路と一致)
    l = [[0]*node_len for i in range(node_len)]

    maxd = initGraph.get_maxd(graph, file_name)

    for i in range(node_len):
        for j in range(node_len):
            if i == j:
                continue
            l[i][j] = d[i][j]
            k[i][j] = 1/(d[i][j]*d[i][j])

    height = maxd if _height == None else _height
    width = maxd if _width == None else _width
    pos = initGraph.get_pos(node_len, width, height)

    for cnt1 in range(loop1):
        max_i = calcDrawInfo.get_max_around_delta(
            pos, k, l, node_len, width, height)
        for cnt2 in range(loop2):
            Exx = 0
            Exy = 0
            Eyy = 0
            Ex = 0
            Ey = 0

            _pos = [[x, y] for x, y in pos]

            diff_x, diff_y, _pos = calcDrawInfo.shift_center(
                _pos, max_i, node_len, width, height)

            for i in range(node_len):
                if i == max_i:
                    continue
                norm = math.sqrt((_pos[max_i][0]-_pos[i][0]) **
                                 2 + (_pos[max_i][1]-_pos[i][1])**2)
                dx_mi = _pos[max_i][0]-_pos[i][0]
                dy_mi = _pos[max_i][1]-_pos[i][1]

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
            pos[max_i] = calcDrawInfo.dorakue(
                pos[max_i], width, height)

    delta = calcDrawInfo.calc_delta_around(pos, k, l, node_len, width, height)
    edge_score = [(d[node2num[str(u)]][node2num[str(v)]] -
                   calcDrawInfo.dist_around(pos, node2num[str(u)], node2num[str(v)], width, height))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, pos, delta, edge_score,
                         node_len, "torus_kame", width, height, file_name)
    kame_log = aestheticsMeasures.calc_evaluation_values(
        delta, edge_score, graph, node2num, pos, l)
    kame_log["wrap"] = calcDrawInfo.get_has_dorakue()

    log.add_log("torus_kame", kame_log)

    return kame_log["dist"]["sum"]
