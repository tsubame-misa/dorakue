import networkx as nx
# from egraph import Graph, DrawingTorus, Rng, FullSgd, eg
import egraph as eg
import matplotlib.pyplot as plt
from common  import drawEgraph, aestheticsMeasures, initGraph


# def torus_sgd(original_graph, file_name, multiple_num=1.0):
#     graph = Graph()

#     indices = {}
#     for u in original_graph.nodes:
#         indices[u] = graph.add_node(u)
#     for u, v in original_graph.edges:
#         graph.add_edge(indices[u], indices[v], (u, v))

#     size = nx.diameter(original_graph)*multiple_num # ここで変わる
#     drawing = DrawingTorus.initial_placement(graph)
#     rng = Rng.seed_from(0)  # random seed
#     sgd = FullSgd(
#         graph,
#         lambda _: 1 / size,  # edge length
#     )
#     scheduler = sgd.scheduler(
#         100,  # number of iterations
#         0.1,  # eps: eta_min = eps * min d[i, j] ^ 2
#     )

#     def step(eta):
#         print(eg.stress(drawing, d))
#         sgd.shuffle(rng)
#         sgd.apply(drawing, eta)
#     scheduler.run(step)

#     pos = {u: (drawing.x(i), drawing.y(i)) for u, i in indices.items()}

#     maxd = initGraph.get_maxd(original_graph, file_name, True, 1/size)
#     d = initGraph.get_shortest_path(original_graph, file_name, True, 1/size)
#     log = aestheticsMeasures.calc_egraph_torus_evaluation_values(original_graph, pos, maxd, d, 1/size)

#     drawEgraph.torus_graph_drawing(pos, original_graph, file_name, False)

#     return log

def torus_sgd(original_graph, file_name, multiple_num=1.0):
    graph = eg.Graph()
    indices = {}
    for u in original_graph.nodes:
        indices[u] = graph.add_node(u)
    for u, v in original_graph.edges:
        graph.add_edge(indices[u], indices[v], (u, v))

    size = nx.diameter(original_graph) * multiple_num
    d = eg.all_sources_bfs(
        graph,
        1 / size, # edge length
    )
    drawing = eg.DrawingTorus.initial_placement(graph)
    rng = eg.Rng.seed_from(0)  # random seed
    sgd = eg.FullSgd.new_with_distance_matrix(d)
    scheduler = sgd.scheduler(
        100,  # number of iterations
        0.1,  # eps: eta_min = eps * min d[i, j] ^ 2
    )

    def step(eta):
        print(eg.stress(drawing, d))
        sgd.shuffle(rng)
        sgd.apply(drawing, eta)
    scheduler.run(step)

    pos = {u: (drawing.x(i) , drawing.y(i)) for u, i in indices.items()}

    maxd = initGraph.get_maxd(original_graph, file_name, True, 1/size)
    d = initGraph.get_shortest_path(original_graph, file_name, True, 1/size)
    log = aestheticsMeasures.calc_egraph_torus_evaluation_values(original_graph, pos, maxd, d, 1/size)

    drawEgraph.torus_graph_drawing(pos, original_graph, file_name, False)

    return log