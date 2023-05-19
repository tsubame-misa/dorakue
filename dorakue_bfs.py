import random
import math
import common


"""
K, Lを除いた版も試してみる？
"""
# 理想の長さと実際の長さ  sum(d[u][v]-dist(u, v) )**2


def dorakue_bfs(graph, _width=None, _height=None):

    def dist(pos, u, v):
        dx = pos[u][0] - pos[v][0]
        dy = pos[u][1] - pos[v][1]
        return (dx ** 2 + dy ** 2) ** 0.5

    def calc_delta(pos,  k, l, node_len):
        Delta = [0]*node_len
        for i in range(node_len):
            Ex = 0
            Ey = 0
            diff_x, diff_y, pos = shift_center(pos, i, node_len)
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
            pos = shift_flat(pos, diff_x, diff_y, node_len)

        return Delta

    def calc_delta_around(pos,  k, l, node_len, width, height):
        Delta = [0]*node_len
        for i in range(node_len):
            Ex = 0
            Ey = 0
            diff_x, diff_y, pos = shift_center(pos, i, node_len)
            for j in range(node_len):
                if i == j:
                    continue
                norm = math.sqrt((pos[i][0]-pos[j][0]) **
                                 2 + (pos[i][1]-pos[j][1])**2)

                dx_ij = pos[i][0] - ((pos[j][0]-(pos[i][0]-width/2) +
                                      width) % width+(pos[j][0]-width/2))
                dy_ij = pos[i][1] - ((pos[j][1]-(pos[i][1]-height/2) +
                                      height) % height+(pos[i][1]-height/2))

                Ex += k[i][j]*dx_ij*(1.0-l[i][j]/norm)
                Ey += k[i][j]*dy_ij*(1.0-l[i][j]/norm)
            Delta[i] = math.sqrt(Ex*Ex+Ey*Ey)
            pos = shift_flat(pos, diff_x, diff_y, node_len)

        return Delta

    def dorakue(pos):
        if pos[0] < 0:
            pos[0] = width+pos[0]
        elif pos[0] > width:
            pos[0] = pos[0]-width

        if pos[1] < 0:
            pos[1] = height+pos[1]
        elif pos[1] > height:
            pos[1] = pos[1]-height

        return pos

    def shift_center(pos, idx, node_len):
        diff_x = pos[idx][0]-width/2
        diff_y = pos[idx][1]-height/2

        for i in range(node_len):
            pos[i][0] -= diff_x
            pos[i][1] -= diff_y
            pos[i] = dorakue(pos[i])

        return diff_x, diff_y, pos

    def shift_flat(pos, diff_x, diff_y, node_len):
        for i in range(node_len):
            pos[i][0] += diff_x
            pos[i][1] += diff_y

            pos[i] = dorakue(pos[i])

        return pos

    # filename = './graph/les_miserables.json'
    # graph = json_graph.node_link_graph(json.load(open(filename)))

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

    print(width, height)
    # posの初期化(ランダム)
    pos = []
    for i in range(node_len):
        x = L0*random.uniform(0, width)
        y = L0*random.uniform(0, height)
        pos.append([x, y])

    for cnt1 in range(50):
        # print(cnt1)
        # 全てのノードに対して中心に持ってきて動かす
        for max_i in range(node_len):
            for cnt2 in range(20):
                Exx = 0
                Exy = 0
                Eyy = 0
                Ex = 0
                Ey = 0

                diff_x, diff_y, pos = shift_center(pos, max_i, node_len)

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
                pos[max_i] = dorakue(pos[max_i])

                pos = shift_flat(pos, diff_x, diff_y, node_len)

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

    print("around")
    delta = calc_delta_around(pos0,  k, l, node_len, width, height)
    edge_score = [(d[node2num[u]][node2num[v]] -
                   common.dist_around(pos, node2num[u], node2num[v], width, height))**2 for u, v in graph.edges]
    common.draw_graph(graph, pos, delta, edge_score,
                      node_len, "dorakue_bfs_around", width, height)
    bfs_around_log = common.calc_evaluation_values(delta, edge_score)
    print(bfs_around_log)

    print("normal")
    delta = calc_delta(pos1,  k, l, node_len)
    edge_score = [(d[node2num[u]][node2num[v]] -
                   dist(pos, node2num[u], node2num[v]))**2 for u, v in graph.edges]
    common.draw_graph(graph, pos, delta, edge_score,
                      node_len, "dorakue_bfs", width, height)
    bfs_log = common.calc_evaluation_values(delta, edge_score)
    print(bfs_log)

    common.add_log("bfs_around", bfs_around_log)
    common.add_log("bfs", bfs_log)
