import networkx as nx
import egraph as eg
import matplotlib.pyplot as plt
from common  import drawEgraph, aestheticsMeasures, initGraph, egraphCalcDrawInfo

def centered_graph(pos, graph):
    min_edge_len = float("inf")
    for p in pos:
        diff_x, diff_y, _pos = egraphCalcDrawInfo.shift_center(pos, p, 1, 1)
        max_edge_len = max(
            egraphCalcDrawInfo.dist_around(_pos, u, v) for u, v in graph.edges)
        if min_edge_len > max_edge_len:
            min_edge_len = max_edge_len
            center_idx = p

    diff_x, diff_y, fin_pos = egraphCalcDrawInfo.shift_center(pos, center_idx, 1, 1)

    return fin_pos


def tuple2array(pos):
    new_pos = {}
    for p in pos:
        new_pos[p] = [pos[p][0], pos[p][1]]
    return new_pos


def torus_sgd(original_graph, file_name, multiple_num=1.0, random_idx=0, time="xxxx", is_chen=False):
    graph = eg.Graph()
    indices = {}
    for u in original_graph.nodes:
        indices[u] = graph.add_node(u)
    for u, v in original_graph.edges:
        graph.add_edge(indices[u], indices[v], (u, v))

    diameter = nx.diameter(original_graph)
    if is_chen:
        multiple_num = (max(diameter, 2) + 1)/diameter

    size = nx.diameter(original_graph) * multiple_num

    d = eg.all_sources_bfs(
        graph,
        1 / size, # edge length
    )
    drawing = eg.DrawingTorus.initial_placement(graph)
    rng = eg.Rng.seed_from(random_idx)  # random seed
    sgd = eg.FullSgd.new_with_distance_matrix(d)
    scheduler = sgd.scheduler(
        20,  # number of iterations
        0.1,  # eps: eta_min = eps * min d[i, j] ^ 2
    )

    def step(eta):
        # print(eg.stress(drawing, d))
        sgd.shuffle(rng)
        sgd.apply(drawing, eta)
    scheduler.run(step)

    s = eg.stress(drawing, d)
    ce = eg.crossing_edges(graph, drawing)
    cn = int(eg.crossing_number(graph, drawing, ce))
    nr = eg.node_resolution(drawing)

    pos = {u: (drawing.x(i) , drawing.y(i)) for u, i in indices.items()}

    array_pos = tuple2array(pos)
    fin_pos = centered_graph(array_pos, original_graph)

    maxd = initGraph.get_maxd(original_graph, file_name, True, 1/size)
    d = initGraph.get_shortest_path(original_graph, file_name, True, 1/size)
    log = aestheticsMeasures.calc_egraph_torus_evaluation_values(original_graph, fin_pos, maxd, d, 1/size)
    log["multiple_num"] = multiple_num
    log["stress"] = s
    log["edge_crossings"] = cn
    log["node_resolution"] = nr
    log["pos"] = fin_pos
    if is_chen:
        log["is_chen"] = True 

    drawEgraph.torus_graph_drawing(fin_pos, original_graph, file_name, multiple_num, time, False)

    return log