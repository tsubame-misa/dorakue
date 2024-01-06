"""
先生のエッジをもとにグラフを描画
"""
import networkx as nx
import egraph as eg
import matplotlib.pyplot as plt
from common  import drawEgraph, aestheticsMeasures, initGraph
import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import torusSGD, egraphTorusSGD
from common import drawGraph, log, initGraph
import re
import matplotlib.pyplot as plt
import math
import os
import shutil
import networkx as nx


def torus_sgd(original_graph, file_name, multiple_num=1.0, random_idx=0, time="xxxx"):
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
    rng = eg.Rng.seed_from(random_idx)  # random seed
    sgd = eg.FullSgd.new_with_distance_matrix(d)
    scheduler = sgd.scheduler(
        100,  # number of iterations
        0.1,  # eps: eta_min = eps * min d[i, j] ^ 2
    )

    def step(eta):
        # print(eg.stress(drawing, d))
        sgd.shuffle(rng)
        sgd.apply(drawing, eta)
    scheduler.run(step)

    s = eg.stress(drawing, d)
    cross = eg.edge_crossings(drawing, d)
    print("cross",cross)

    pos = {u: (drawing.x(i) , drawing.y(i)) for u, i in indices.items()}

    maxd = initGraph.get_maxd(original_graph, file_name, True, 1/size)
    d = initGraph.get_shortest_path(original_graph, file_name, True, 1/size)
    log = aestheticsMeasures.calc_egraph_torus_evaluation_values(original_graph, pos, maxd, d, 1/size)
    log["multiple_num"] = multiple_num
    log["stress"] = s
    log["pos"] = pos

    drawEgraph.torus_graph_drawing(pos, original_graph, file_name, multiple_num, time, False)

    return log



def main():
    files = glob.glob("./graph/*")
    # files = glob.glob("./chen2021Graph/*")
    # files = glob.glob("./scallFreeGraph2/*")
    # files = glob.glob("./dwtGraph/*")
    # files = glob.glob("./doughNetGraph/default/*")

    # 使用するグラフをノード数順に並び替える
    graphs = []
    for filepath in files:
        if filepath[-3:]=="txt":
            continue
        print(filepath, filepath[-3:])
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/.]', filepath)[3]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    
    log_file_name = "uuu"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        print(g["name"], "size", len(g["graph"].nodes))
        if not g["name"]=="petersen":
            continue
        time = setup.get_time()
        index_time = str(0) + str(time)
        drawGraph.set_time(index_time)
        chen_log =  egraphTorusSGD.torus_sgd(g["graph"], g["name"]+"-our", 1, 0, index_time, True)
        our_log =  egraphTorusSGD.torus_sgd(g["graph"],  g["name"]+"-chen", 1.80751766602255, 0, index_time)
        # print(_log["stress"], _log["edge_length_variance"], _log["edge_crossings"], _log["minimum_angle"])

        print(chen_log["stress"]/our_log["stress"], chen_log["stress"], our_log["stress"])

        # nx.draw_networkx(g["graph"], node_size=5, with_labels=None, width=0.5)
        # plt.show()
        exit()


if __name__ == '__main__':
    main()