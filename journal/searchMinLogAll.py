import argparse
import glob
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent) + "/")

import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import egraphTorusSGD
from common import drawGraph, log
import re
import matplotlib.pyplot as plt
import os
import math
from common import log, initGraph
import networkx as nx

"""
lenの変化でstessがどう変わるか線形探索
全てのログを保存
"""


COUNT = 80
LOOP = 20


def create_graph(graph, file_name, dir_name, multiple_num, i, weigthing):
    time = setup.get_time()
    index_time = str(i) + str(time)
    drawGraph.set_time(index_time)
    torus_log = egraphTorusSGD.torus_sgd(
        graph, file_name, dir_name, multiple_num, i, index_time, weigthing=weigthing
    )
    return torus_log


def save_graph(data, x, optimal_cell, chen_cell_size, dir_name, name, metrics):
    # 折れ線グラフの描画
    plt.figure(figsize=(10, 6))
    plt.plot(x, data)
    plt.title(name + " " + metrics)
    plt.axvline(x=optimal_cell, color="red")
    plt.axvline(x=chen_cell_size, color="green")
    # plt.show()
    img_path = (
        "./"
        + dir_name
        + "/metrics_liner/"
        + metrics
        + "/"
        + name
        + "-"
        + metrics
        + ".png"
    )
    plt.savefig(img_path)


def get_stress_by_len(graph, file_name, dir_name, weigthing, loop):
    data = []
    all_log = {}
    for i in range(1, COUNT + 1):
        initGraph.clear()
        n = math.floor(i * 0.05 * 100) / 100
        for j in range(loop):
            print(file_name, n)
            torus_log = create_graph(graph, file_name, dir_name, n, j, weigthing)
            data.append([n, torus_log["stress"]])
            if n in all_log:
                all_log[n].append(torus_log)
            else:
                all_log[n] = [torus_log]

    return all_log


"""
graph_file_dir_path, log_file_path, weigthing=True/False
# files = ./graphSet/networkx/
# files = ./graphSet/doughNetGraph/default/
# files = ./graphSet/randomPartitionNetwork /
# files = ./graphSet/suiteSparse/
"""


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("graph_file_name")
    parser.add_argument("log_file_name")
    parser.add_argument("--weigthing", action="store_true")
    parser.add_argument("--loop", default=20, type=int)
    parser.add_argument("--file_only", action="store_true")

    args = parser.parse_args()

    if args.file_only:
        files = [args.graph_file_name]
    else:
        files = glob.glob("./" + args.graph_file_name + "/*")

    searach_min_log_all(files, args.log_file_name, args.weigthing, args.loop)


def searach_min_log_all(files, log_file_name, weigthing, loop):
    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split("[/]", filepath)[-1][:-5]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)

    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        if os.path.isfile(log_file_name + "/log/" + g["name"] + "-.json"):
            continue
        print(g["name"], "size", len(g["graph"].nodes), "weighting", weigthing)
        all_log = get_stress_by_len(
            g["graph"], g["name"], log_file_name, weigthing, loop
        )
        optimal_cell_size = create_metrics_graph(
            all_log, g["graph"], log_file_name, g["name"]
        )
        log.create_log(
            {"optimal_cell_size": optimal_cell_size, "data": all_log}, g["name"]
        )


def create_metrics_graph(data_dict, graph, new_dir_path, name):
    diameter = nx.diameter(graph)
    chen_cell_size = (max(diameter, 2) + 1) / diameter

    x_idx = [x for x in data_dict.keys()]
    metrics = [
        "stress",
        "ideal_edge_lengths",
        "edge_crossings",
        "crossing_angle_maximization",
        "node_resolution",
    ]
    liner_dict = {
        "stress": [],
        "ideal_edge_lengths": [],
        "edge_crossings": [],
        "crossing_angle_maximization": [],
        "node_resolution": [],
    }
    for x in x_idx:
        x_data = data_dict[x]
        n = len(x_data)
        for m in metrics:
            x_data_m = sorted([d[m] for d in x_data])
            liner_dict[m].append(x_data_m[n // 2])

    best_stress_comp = min(liner_dict["stress"])
    best_idx = liner_dict["stress"].index(best_stress_comp)
    optimal_cell_size = x_idx[best_idx]

    if not os.path.isdir(new_dir_path + "/metrics_liner"):
        os.mkdir(new_dir_path + "/metrics_liner")

    for f in metrics:
        path = new_dir_path + "/metrics_liner/" + f
        if not os.path.isdir(path):
            os.mkdir(path)

    for m in metrics:
        save_graph(
            liner_dict[m],
            x_idx,
            optimal_cell_size,
            chen_cell_size,
            new_dir_path,
            name,
            m,
        )
    return optimal_cell_size


if __name__ == "__main__":
    main()
