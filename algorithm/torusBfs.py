import math
from common import drawGraph, aestheticsMeasures,  calcDrawInfo
import setup


def torus_bfs(graph, _width=None, _height=None):
    node_len = len(graph.nodes)

    node2num = dict()
    cnt = 0
    for node in graph.nodes:
        node2num[node] = cnt
        cnt += 1

    # 隣接行列の初期化
    d = [[float('inf')]*node_len for i in range(node_len)]
    adjacent_node = [[]*node_len for i in range(node_len)]
    # 隣接行列の作成
    for i in range(node_len):
        d[i][i] = 0
    for x_node, y_node in graph.edges:
        # 重みがないので1
        x = node2num[x_node]
        y = node2num[y_node]
        d[x][y] = 100
        d[y][x] = 100
        adjacent_node[x].append(y)
        adjacent_node[y].append(x)

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

    L0 = 1
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

    # height = maxd*(1/(2**0.5))
    # width = maxd*(1/(2**0.5))
    height = maxd if _height == None else _height
    width = maxd if _width == None else _width

    pos = initGraph.get_pos(node_len, width, height)

    loop1, loop2 = setup.get_loop()

    for cnt1 in range(loop1):
        # 全てのノードに対して中心に持ってきて動かす
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

    q = [0]
    visited = [0]
    while len(q) > 0:
        u = q.pop()
        for v in adjacent_node[u]:
            if v not in visited:
                pos[v][0] = (pos[v][0]-(pos[u][0]-width/2) +
                             width) % width+(pos[u][0]-width/2)
                pos[v][1] = (pos[v][1]-(pos[u][1]-height/2) +
                             height) % height+(pos[u][1]-height/2)
                visited.append(v)
                q.append(v)

    pos0 = [[x, y] for x, y in pos]
    pos1 = [[x, y] for x, y in pos]

    delta = calcDrawInfo.calc_delta_around(
        pos0,  k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                   calcDrawInfo.dist_around(pos, node2num[u], node2num[v], width, height))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, pos, delta, edge_score,
                         node_len, "dorakue_bfs_around", width, height)
    bfs_around_log = aestheticsMeasures.calc_evaluation_values(
        delta, edge_score)

    delta = calcDrawInfo.calc_delta(pos1,  k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                   calcDrawInfo.dist(pos, node2num[u], node2num[v]))**2 for u, v in graph.edges]
    drawGraph.draw_graph(graph, pos, delta, edge_score,
                         node_len, "dorakue_bfs", width, height)
    bfs_log = aestheticsMeasures.calc_evaluation_values(delta, edge_score)

    # ドラクエのログは同じになるのでcenterの方だけ見ればいい
    # log.add_log("bfs_around", bfs_around_log)
    # log.add_log("bfs", bfs_log)

    return min(bfs_log["dist"]["sum"], bfs_around_log["dist"]["sum"])
