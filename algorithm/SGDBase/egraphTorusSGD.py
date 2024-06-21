import os
import networkx as nx
import egraph as eg
import matplotlib.pyplot as plt
import networkx as nx
import egraph as eg
import matplotlib.pyplot as plt


def torus_sgd(
    original_graph,
    name,
    dir,
    multiple_num=1.0,
    random_idx=0,
    time="xxxx",
    is_chen=False,
):
    graph = eg.Graph()
    indices = {}
    for u in original_graph.nodes:
        indices[u] = graph.add_node(u)
    for u, v in original_graph.edges:
        graph.add_edge(indices[u], indices[v], (u, v))

    diameter = nx.diameter(original_graph)
    if is_chen:
        multiple_num = (max(diameter, 2) + 1) / diameter

    size = nx.diameter(original_graph) * multiple_num
    d = eg.all_sources_bfs(
        graph,
        1 / size,  # edge length
    )
    drawing = eg.DrawingTorus2d.initial_placement(graph)
    rng = eg.Rng.seed_from(random_idx)  # random seed
    sgd = eg.FullSgd.new_with_distance_matrix(d)
    scheduler = sgd.scheduler(
        100,  # number of iterations
        0.1,  # eps: eta_min = eps * min d[i, j] ^ 2
    )

    def step(eta):
        sgd.shuffle(rng)
        sgd.apply(drawing, eta)

    scheduler.run(step)

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
        original_graph, pos, ax=ax, node_color="#6f6f6fcf", node_size=50
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
        + time
        + ".png"
    )
    plt.savefig(img_path)

    ec = eg.crossing_edges(graph, drawing)
    log = {
        "multiple_num": multiple_num,
        "stress": eg.stress(drawing, d),
        "ideal_edge_lengths": eg.ideal_edge_lengths(graph, drawing, d),
        "edge_crossings": eg.crossing_number_with_crossing_edges(ec),
        "crossing_angle_maximazation": eg.crossing_angle_with_crossing_edges(ec),
        "node_resolution": eg.node_resolution(drawing),
        "pos": pos,
    }
    return log
