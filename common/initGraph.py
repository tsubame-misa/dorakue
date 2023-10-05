import setup
from functools import cache
import random
import itertools
import networkx as nx


SHORTEST_PATH = dict()
POS = []
PAIR_INDEX = []
DORAKUE = False


def clear():
    global POS, PAIR_INDEX, SHORTEST_PATH
    POS = []
    PAIR_INDEX = []
    SHORTEST_PATH = dict()


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


def warshall(d, node_len):
    for k in range(node_len):
        for i in range(node_len):
            for j in range(node_len):
                d[i][j] = min(d[i][j], d[i][k]+d[k][j])
    return d


@cache
def get_node2num_memoized(graph):
    node2num = dict()
    cnt = 0
    for node in graph.nodes:
        node2num[str(node)] = cnt
        cnt += 1
    return node2num


def get_shortest_path(graph, node_len, node2num, file_name):
    # メモ化
    if file_name in SHORTEST_PATH:
        return SHORTEST_PATH[file_name]

    UNIT_EDGE_LENGTH = setup.get_edge_width()
    d = dict(nx.all_pairs_dijkstra_path_length(
        graph, weight=lambda u, v, e: UNIT_EDGE_LENGTH))

    # 辞書に保存
    SHORTEST_PATH[file_name] = d
    return d


def init_pos(node_len, width, height):
    global POS
    L0 = 1
    # 範囲を固定
    l = 100
    # l = 1000
    for i in range(node_len):
        x = L0*random.uniform(width/2-l/2, width/2+l/2)
        y = L0*random.uniform(height/2-l/2, height/2+l/2)
        POS.append([x, y])


def get_pos(node_len, width, height):
    global POS
    if len(POS) == 0:
        init_pos(node_len, width, height)
    pos0 = [[x, y] for x, y in POS]
    return pos0


def init_pair_index(graph, loop):
    for i in range(loop):
        pair_index = [list(p) for p in itertools.combinations(
            [i for i in graph.nodes], 2)]
        pair_index = random.sample(pair_index, len(pair_index))
        PAIR_INDEX.append(pair_index)


def get_random_pair(graph, loop, t):
    global PAIR_INDEX
    if len(PAIR_INDEX) == 0:
        init_pair_index(graph, loop)
    pair_index = [[x, y] for x, y in PAIR_INDEX[t]]
    return pair_index


@cache
def get_maxd(graph, file_name):
    node_len = len(graph.nodes)
    node2num = get_node2num_memoized(graph)

    # 最短経路
    d = get_shortest_path(graph, node_len, node2num, file_name)
    # 重み(バネの強さ)
    k = [[0]*node_len for i in range(node_len)]

    maxd = 0
    # for i in range(node_len):
    #     for j in range(node_len):
    #         if maxd < d[i][j]:
    #             maxd = d[i][j]
    for val in d.values():
        _max = max([v for v in val.values()])
        if _max > maxd:
            maxd = _max

    return maxd
