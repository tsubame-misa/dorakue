import math
import os
import networkx as nx
import egraph as eg
import matplotlib.pyplot as plt


class Scheduler:
    # ここをlinerにしてみる？
    # もう少し始めを緩やかに落としてみても良いかも？
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


def optimize(sgd, drawing, etas, size, idx):
    for eta in etas:
        rng2 = eg.Rng.seed_from(int(size * 100 // 1 * idx))
        sgd.shuffle(rng2)
        sgd.apply(drawing, eta / size**2)


def show_stress_graph(x, y, file_name, dir_name):
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(x, y, marker="o", label="stress", linestyle="-", color="r")

    # ラベルやタイトルの設定
    plt.xlabel("cell size")
    plt.title(file_name)
    plt.legend()  # 凡例を表示

    new_dir_path = "./" + dir_name + "/stress_by_len/"

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_path = "./" + dir_name + "/stress_by_len/" + file_name + ".png"
    plt.savefig(img_path)


def cell_optimazation_3_search(
    original_graph, name, dir, idx=0, time="xxxx", weigthing=False
):
    graph = eg.Graph()
    indices = {}
    for u in original_graph.nodes:
        indices[u] = graph.add_node(u)
    for u, v in original_graph.edges:
        graph.add_edge(indices[u], indices[v], (u, v))

    n = graph.node_count()

    if weigthing:
        d = eg.all_sources_dijkstra(graph, Weighting(graph))
    else:
        d = eg.all_sources_dijkstra(graph, lambda _: 1)

    diameter = max(
        d.get(u, v) for u in graph.node_indices() for v in graph.node_indices()
    )

    gss_iterations = 8
    sgd_iterations = 5
    eps = 0.1
    t_max = gss_iterations * sgd_iterations

    if weigthing:
        distance = eg.all_sources_dijkstra(graph, lambda _: 1)
        w_min = (
            1
            / min(
                distance.get(i, j) / diameter
                for i in range(n)
                for j in range(n)
                if distance.get(i, j) != 0
            )
            ** 2
        )
        w_max = (
            1
            / max(
                distance.get(i, j) / diameter
                for i in range(n)
                for j in range(n)
                if distance.get(i, j) != 0
            )
            ** 2
        )
    else:
        distance = eg.all_sources_dijkstra(graph, lambda _: 1)
        w_min = (
            1
            / min(
                distance.get(i, j)
                for i in range(n)
                for j in range(n)
                if distance.get(i, j) != 0
            )
            ** 2
        )
        w_max = (
            1
            / max(
                distance.get(i, j)
                for i in range(n)
                for j in range(n)
                if distance.get(i, j) != 0
            )
            ** 2
        )

    scheduler = Scheduler(w_min, eps / w_max, t_max)
    eta = [scheduler(t) for t in range(t_max)]

    # 0-3.5が丁度良さそう
    low = 0
    high = 3.5
    lr_diff = high - low
    x = lr_diff / 3

    if weigthing:
        distance = eg.all_sources_dijkstra(graph, Weighting(graph))
    else:
        distance = eg.all_sources_dijkstra(graph, lambda _: 1)

    m1 = x
    low_drawing = eg.DrawingTorus2d.initial_placement(graph)
    low_distance = eg.DistanceMatrix(graph)
    for i in range(n):
        for j in range(n):
            low_distance.set(i, j, distance.get(i, j) / (diameter * m1))
    low_sgd = eg.FullSgd.new_with_distance_matrix(low_distance)
    optimize(low_sgd, low_drawing, eta[:sgd_iterations], diameter * m1, idx)

    m2 = high - x
    high_drawing = eg.DrawingTorus2d.initial_placement(graph)
    high_distance = eg.DistanceMatrix(graph)
    for i in range(n):
        for j in range(n):
            high_distance.set(i, j, distance.get(i, j) / (diameter * m2))
    high_sgd = eg.FullSgd.new_with_distance_matrix(high_distance)
    optimize(high_sgd, high_drawing, eta[:sgd_iterations], diameter * m2, idx)

    data = [
        [m1, eg.stress(low_drawing, low_distance)],
        [m2, eg.stress(high_drawing, high_distance)],
    ]

    for i in range(1, gss_iterations):
        # print(m1, m2)
        if eg.stress(low_drawing, low_distance) > eg.stress(
            high_drawing, high_distance
        ):
            data.append([m1, eg.stress(low_drawing, low_distance)])
            low = m1
            m1 = m2
            m2 = high - x

            # low <- high
            for i in range(n):
                low_drawing.set_x(i, high_drawing.x(i))
                low_drawing.set_y(i, high_drawing.y(i))
                for j in range(n):
                    low_distance.set(i, j, high_distance.get(i, j))
            low_sgd = high_sgd
            optimize(
                low_sgd,
                low_drawing,
                eta[i * sgd_iterations : (i + 1) * sgd_iterations],
                diameter * m2,
                idx,
            )

            # high <- high - (lr_diff - 2 * x)
            for i in range(n):
                for j in range(n):
                    high_distance.set(i, j, high_distance.get(i, j) * m1 / m2)
            high_sgd = eg.FullSgd.new_with_distance_matrix(high_distance)
            optimize(
                high_sgd,
                high_drawing,
                eta[i * sgd_iterations : (i + 1) * sgd_iterations],
                diameter * m2,
                idx,
            )
        else:
            data.append([m2, eg.stress(high_drawing, high_distance)])
            high = m2
            m2 = m1
            m1 = low + x

            # high <- low
            for i in range(n):
                high_drawing.set_x(i, low_drawing.x(i))
                high_drawing.set_y(i, low_drawing.y(i))
                for j in range(n):
                    high_distance.set(i, j, low_distance.get(i, j))
            high_sgd = low_sgd
            optimize(
                high_sgd,
                high_drawing,
                eta[i * sgd_iterations : (i + 1) * sgd_iterations],
                diameter * m2,
                idx,
            )

            # low <- low + (lr_diff - 2 * x)
            for i in range(n):
                for j in range(n):
                    low_distance.set(i, j, low_distance.get(i, j) * m2 / m1)
            low_sgd = eg.FullSgd.new_with_distance_matrix(low_distance)
            optimize(
                low_sgd,
                low_drawing,
                eta[i * sgd_iterations : (i + 1) * sgd_iterations],
                diameter * m2,
                idx,
            )

        lr_diff = high - low
        x = lr_diff / 3
    if eg.stress(low_drawing, low_distance) > eg.stress(high_drawing, high_distance):
        drawing = high_drawing
        size = m2
        stress = eg.stress(high_drawing, high_distance)
        ideal_edge_lengths = eg.ideal_edge_lengths(graph, drawing, high_distance)
        data.append([m2, eg.stress(high_drawing, high_distance)])
    else:
        drawing = low_drawing
        size = m1
        stress = eg.stress(low_drawing, low_distance)
        ideal_edge_lengths = eg.ideal_edge_lengths(graph, drawing, low_distance)
        data.append([m1, eg.stress(low_drawing, low_distance)])

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
        original_graph, pos, ax=ax, node_color="#6f6f6fcf", node_size=100
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
        + str(size)
        + "-"
        + time
        + ".png"
    )
    plt.savefig(img_path)

    sorted_data = sorted(data, key=lambda x: x[0])
    show_stress_graph(
        [row[0] for row in sorted_data],
        [row[1] for row in sorted_data],
        name + str(time),
        dir,
    )

    print("size", size)

    ec = eg.crossing_edges(graph, drawing)
    log = {
        "multiple_num": size,
        "stress": stress,
        "ideal_edge_lengths": ideal_edge_lengths,
        "edge_crossings": eg.crossing_number_with_crossing_edges(ec),
        "crossing_angle_maximization": eg.crossing_angle_with_crossing_edges(ec),
        "node_resolution": eg.node_resolution(drawing),
        "pos": pos,
    }

    return log
    # plt.savefig('tmp/sgd_torus_cell_optimization.png')
