import math
from common import drawGraph, log, calcDrawInfo, debug, aestheticsMeasures
import setup
import itertools
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
                if i != p and (not (p, i) in pair_index) and (not (i, p) in pair_index):
                    # ここ逆にするとバグる
                    pair_index.add((p, i))
        pair_index = random.sample(pair_index, len(pair_index))
        return pair_index

    index = []
    height = 300 if _height == None else _height
    width = 300 if _width == None else _width
    edge_len = 100

    node_len = len(graph.nodes)
    h = node_len
    h = 10

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
        l[i][i] = 0
    for x_node, y_node in graph.edges:
        # 重みがないので1
        x = node2num[x_node]
        y = node2num[y_node]
        l[x][y] = edge_len
        l[y][x] = edge_len

    P = []
    pivot = random.randint(0, node_len)
    # pivot = 0
    P.append(pivot)
    d[pivot] = dijkstra(l, pivot)
    m = d[pivot].copy()
    for i in range(h-1):
        _index = m.index(max(m))
        d[_index] = dijkstra(l, _index)
        P.append(_index)
        for j in range(node_len):
            m[j] = min(m[j], d[_index][j])

    for p in P:
        wd[p] = [0]*node_len

    # 隣接行列の初期化
    k = [[0]*node_len for i in range(node_len)]
    w = [[1]*node_len for i in range(node_len)]

    for i in range(node_len):
        for j in P:
            if d[j][i] != 0:
                w[j][i] = pow(d[j][i], -2)

    # ピボットの中で一番近いもの
    near_pivot = []
    for i in range(node_len):
        v = []
        if i in P:
            near_pivot.append([])
            continue
        for p in P:
            if p != i:
                v.append(d[p][i])
            else:
                v.append(float("inf"))
        # print(v)
        # print("min v", min(v), P[v.index(min(v))])
        # near_pivot.append(P[v.index(min(v))])
        _near_pivot = []
        _min = min(v)
        for j in range(h):
            if v[j] == _min:
                _near_pivot.append(P[j])
        near_pivot.append(_near_pivot)
        # print(_near_pivot)

    print(wd[P[0]][2], wd[2][P[0]])

    for i in range(node_len):
        for p in P:
            near_i = [j for j, x in enumerate(l[i]) if x == 100]
            # near_p = [i for i, x in enumerate(l[p]) if x == 100]
            # near_p = [i for i, x in enumerate(near_pivot) if x == p]
            near_p = [i for i in range(node_len) if p in near_pivot[i]]

            # pがiの近傍じゃなかったら
            if not p in near_i:
                # s = len(d_pj < dpi) jはpに近い頂点セット
                if len(near_p) > 0:
                    cnt = 0
                else:
                    cnt = 1
                # print(near_p)
                for j in near_p:
                    if d[p][j] <= d[p][i]/2:
                        cnt += 1
                d[i] = dijkstra(l, i)
                if d[i][p] != 0:
                    w[i][p] = pow(d[i][p], -2)
                wd[i][p] = w[i][p]*cnt

    print(P)
    print(wd[P[0]][2], wd[2][P[0]])

    for x_node, y_node in graph.edges:
        i = node2num[x_node]
        j = node2num[y_node]
        d[i] = dijkstra(l, node2num[x_node])
        wd[i][j] = w[i][j]
        wd[j][i] = w[i][j]
        k[i][j] = 1 / (d[i][j] * d[i][j])

    pos = initGraph.get_pos(node_len, width, height)

    loop1, loop2 = setup.get_loop()

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
            mu_i = min(wd[i][j]*eta, 1)
            mu_j = min(wd[j][i]*eta, 1)

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
    kame_log = aestheticsMeasures.calc_evaluation_values(delta, edge_score)

    debug.add_node_a(pos)
    debug.add_index_a(index)

    log.add_log("sparseSGD", kame_log)

    return kame_log["dist"]["sum"]
