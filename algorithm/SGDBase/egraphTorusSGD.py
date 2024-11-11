import os
import networkx as nx
import egraph as eg
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import math


class Scheduler:
    def __init__(self, eta_max, eta_min, t_max):
        self.a = eta_max
        self.b = math.log(eta_min / eta_max) / (t_max - 1)

    def __call__(self, t):
        return self.a * math.exp(self.b * t)


class Weighting:
    def __init__(self, graph):
        self.graph = graph

    def __call__(self, e):
        u, v = self.graph.edge_endpoints(e)
        u_set = set(self.graph.neighbors(u))
        v_set = set(self.graph.neighbors(v))
        return len(u_set | v_set) - len(u_set & v_set)


def optimize(sgd, drawing, etas, size):
    for eta in etas:
        rng2 = eg.Rng.seed_from(int(size * 100 // 1))
        sgd.shuffle(rng2)
        sgd.apply(drawing, eta / size**2)


def torus_sgd(
    original_graph,
    name,
    dir,
    multiple_num=1.0,
    time="xxxx",
    is_chen=False,
    weigthing=False,
    node_size=10,
):
    graph = eg.Graph()
    indices = {}
    for u in original_graph.nodes:
        indices[u] = graph.add_node(u)
    for u, v in original_graph.edges:
        graph.add_edge(indices[u], indices[v], (u, v))

    n = graph.node_count()

    if weigthing:
        distance = eg.all_sources_dijkstra(graph, Weighting(graph))
    else:
        distance = eg.all_sources_dijkstra(graph, lambda _: 1)

    diameter = max(
        distance.get(u, v) for u in graph.node_indices() for v in graph.node_indices()
    )

    eps = 0.1
    t_max = 20

    if weigthing:
        w_min = (
            1
            / max(
                distance.get(i, j)
                for i in range(n)
                for j in range(n)
                if distance.get(i, j) != 0
            )
            ** 2
        )
        w_max = (
            1
            / min(
                distance.get(i, j)
                for i in range(n)
                for j in range(n)
                if distance.get(i, j) != 0
            )
            ** 2
        )
    else:
        w_min = (
            1
            / max(
                distance.get(i, j)
                for i in range(n)
                for j in range(n)
                if distance.get(i, j) != 0
            )
            ** 2
        )
        w_max = (
            1
            / min(
                distance.get(i, j)
                for i in range(n)
                for j in range(n)
                if distance.get(i, j) != 0
            )
            ** 2
        )

    scheduler = Scheduler(1 / w_min, eps / w_max, t_max)
    eta = [scheduler(t) for t in range(t_max)]

    if is_chen:
        # weigthingだと +1 の分の長さが不明なのでどうしたら良いかなという
        # 平均, 最小値
        multiple_num = (max(diameter, 2) + 1) / diameter
    size = multiple_num

    drawing = eg.DrawingTorus2d.initial_placement(graph)
    distance_matrix = eg.DistanceMatrix(graph)
    for i in range(n):
        for j in range(n):
            distance_matrix.set(i, j, distance.get(i, j) / (diameter * size))
    sgd = eg.FullSgd.new_with_distance_matrix(distance_matrix)
    optimize(sgd, drawing, eta[:t_max], diameter * size)

    pos = {u: (drawing.x(i) * size, drawing.y(i) * size) for u, i in indices.items()}
    nx_edge_graph = nx.Graph()
    edge_pos = {}
    for e in graph.edge_indices():
        u, v = graph.edge_endpoints(e)
        segments = drawing.edge_segments(u, v)
        for i, ((x1, y1), (x2, y2)) in enumerate(segments):
            eu = f"{u}:{v}:{i}:0"
            ev = f"{u}:{v}:{i}:1"
            nx_edge_graph.add_edge(eu, ev)
            edge_pos[eu] = (x1 * size, y1 * size)
            edge_pos[ev] = (x2 * size, y2 * size)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    nx.draw_networkx_nodes(
        original_graph, pos, ax=ax, node_color="#6f6f6fcf", node_size=node_size
    )
    nx.draw_networkx_edges(nx_edge_graph, edge_pos, ax=ax)

    if not os.path.isdir(dir):
        os.mkdir(dir)

    img_path = (
        "./"
        + dir
        + "/torusSGD_wrap/"
        + str(name)
        + "-"
        + str(multiple_num)
        + "-"
        + str(time)
        + ".png"
    )
    plt.savefig(img_path)

    ec = eg.crossing_edges(graph, drawing)

    log = {
        "multiple_num": multiple_num,
        "stress": eg.stress(drawing, distance_matrix),
        "ideal_edge_lengths": eg.ideal_edge_lengths(graph, drawing, distance_matrix),
        "edge_crossings": eg.crossing_number_with_crossing_edges(ec),
        "crossing_angle_maximization": eg.crossing_angle_with_crossing_edges(ec),
        "node_resolution": eg.node_resolution(drawing),
        "pos": pos,
    }
    return log
