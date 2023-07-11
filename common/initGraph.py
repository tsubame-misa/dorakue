from functools import lru_cache
import setup
from collections import defaultdict


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


@lru_cache(maxsize=1000)
def get_node2num_memoized(graph):
    node2num = dict()
    cnt = 0
    for node in graph.nodes:
        node2num[str(node)] = cnt
        cnt += 1
    return node2num


# @lru_cache(maxsize=1000)
# 自前メモ化の必要ある？
def get_shortest_path(graph, node_len, node2num):
    edge_weight = setup.get_edge_width()
    d = [[float('inf')]*node_len for i in range(node_len)]

    for i in range(node_len):
        d[i][i] = 0
    for x_node, y_node in graph.edges:
        x = node2num[x_node]
        y = node2num[y_node]
        d[x][y] = edge_weight
        d[y][x] = edge_weight

    # ワーシャルフロイド(最短経路)
    for i in range(node_len):
        d[i] = dijkstra(d, i)

    return d
