from functools import lru_cache


@lru_cache(maxsize=1000)
def get_node2num_memoized(graph):
    node2num = dict()
    cnt = 0
    for node in graph.nodes:
        node2num[node] = cnt
        cnt += 1
    return node2num
