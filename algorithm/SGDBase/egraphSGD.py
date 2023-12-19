import networkx as nx
import egraph as eg
from common import initGraph, aestheticsMeasures, drawGraph


def sgd(original_graph, file_name, random_idx=0):
    graph = eg.Graph()
    indices = {}
    for u in original_graph.nodes:
        indices[u] = graph.add_node(u)
    for u, v in original_graph.edges:
        graph.add_edge(indices[u], indices[v], (u, v))

    size = nx.diameter(original_graph) 
    d = eg.all_sources_bfs(
        graph,
        1 / size, # edge length
    )

    drawing = eg.Drawing2D.initial_placement(graph)
    rng = eg.Rng.seed_from(random_idx)  # random seed
    sgd = eg.FullSgd(
        graph,
        lambda _: 1/size,  # edge length
    )
    scheduler = sgd.scheduler(
        100,  # number of iterations
        0.1,  # eps: eta_min = eps * min d[i, j] ^ 2
    )

    def step(eta):
        sgd.shuffle(rng)
        sgd.apply(drawing, eta)
    scheduler.run(step)
    s = eg.stress(drawing, d)

    pos = {u: (drawing.x(i), drawing.y(i)) for u, i in indices.items()}
    
    maxd = initGraph.get_maxd(original_graph, file_name, True, 1/size)
    d = initGraph.get_shortest_path(original_graph, file_name, True, 1/size)
    log = aestheticsMeasures.calc_egraph_torus_evaluation_values(original_graph, pos, maxd, d, 1/size)
    log["stress"] = s
    log["pos"] = pos

    drawGraph.create_and_save_graph(original_graph, pos, "#88888899", "#888888", "SGD", 1, 1, file_name)

    return log

