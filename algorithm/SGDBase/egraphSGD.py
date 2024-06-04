import os
import networkx as nx
import egraph as eg
import matplotlib.pyplot as plt

def sgd(original_graph, file_name, dir_name,  random_idx=0, time="xxxx", ):
    graph = eg.Graph()
    indices = {}
    for u in original_graph.nodes:
        indices[u] = graph.add_node(u)
    for u, v in original_graph.edges:
        graph.add_edge(indices[u], indices[v], (u, v))

    drawing = eg.DrawingEuclidean2d.initial_placement(graph)
    rng = eg.Rng.seed_from(random_idx)  # random seed
    size = nx.diameter(original_graph) 
    sgd = eg.SparseSgd(
        graph,
        lambda _: 1/size,  # edge length
        50,  # number of pivots
        rng,
    )
    scheduler = sgd.scheduler(
        20,  # number of iterations
        0.1,  # eps: eta_min = eps * min d[i, j] ^ 2
    )

    def step(eta):
        sgd.shuffle(rng)
        sgd.apply(drawing, eta)
    scheduler.run(step)

    pos = {u: (drawing.x(i), drawing.y(i)) for u, i in indices.items()}
    
    G = nx.DiGraph()
    G.add_nodes_from(original_graph.nodes)
    G.add_edges_from(original_graph.edges)
    plt.figure(figsize=(12, 12))
    nx.draw_networkx(G, pos, False, with_labels=False,
                     node_color="#88888899", edge_color="#888888", node_size=20, font_size=5)

    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    img_path ='./'+dir_name+'/SGD/' + \
        str(file_name) + '-' + time + '.png'
    plt.savefig(img_path)

    d = eg.all_sources_bfs(
        graph,
        1 / size, # edge length
    )

    ec = eg.crossing_edges(graph, drawing)
    log = {"multiple_num": -1, 
           "stress": eg.stress(drawing, d) , 
           "edge_crossings":eg.crossing_number_with_crossing_edges(ec),
           "minimum_angle": eg.crossing_angle_with_crossing_edges(ec), 
           "node_resolution":eg.node_resolution(drawing), 
           "pos":pos}
    return log