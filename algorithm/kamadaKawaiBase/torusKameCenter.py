import math
from common import drawGraph
from common import log
from common import calcDrawInfo
import setup


def torus_kame(graph, _width=None, _height=None):
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

    for cnt1 in range(loop1):
        max_i = calc_delta(pos, k, l, node_len, width, height)
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

    delta = calcDrawInfo.calc_delta(pos, k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                   calcDrawInfo.dist(pos, node2num[u], node2num[v]))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, pos, delta, edge_score,
                         node_len, "torus_kame", width, height)
    kame_log = log.calc_evaluation_values(delta, edge_score)

    log.add_log("torus_kame", kame_log)

    return kame_log["dist"]["sum"]
