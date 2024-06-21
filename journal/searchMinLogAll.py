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


def create_graph(graph, file_name, dir_name, multiple_num, i):
    time = setup.get_time()
    index_time = str(i) + str(time)
    drawGraph.set_time(index_time)
    torus_log = egraphTorusSGD.torus_sgd(
        graph, file_name, dir_name, multiple_num, i, index_time
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


def get_stress_by_len(graph, file_name, dir_name):
    data = []
    all_log = {}
    for i in range(1, COUNT + 1):
        initGraph.clear()
        n = math.floor(i * 0.05 * 100) / 100
        for j in range(20):
            print(file_name, n)
            torus_log = create_graph(graph, file_name, dir_name, n, j)
            data.append([n, torus_log["stress"]])
            if n in all_log:
                all_log[n].append(torus_log)
            else:
                all_log[n] = [torus_log]

    log.create_log(all_log, file_name)
    return all_log


def main():
    # files = glob.glob("./graphSet/networkx/*")
    # files = glob.glob("./graphSet/doughNetGraph/default/*")
    # files = glob.glob("./graphSet/randomPartitionNetwork /*")
    files = glob.glob("./graphSet/suiteSparse/*")

    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split("[/]", filepath)[-1][:-5]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)

    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    log_file_name = "metrics_liner_sparse"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        if os.path.isfile("./metrics_liner_sparse/log/" + g["name"] + "-.json"):
            continue
        print(g["name"], "size", len(g["graph"].nodes))
        # try:
        all_log = get_stress_by_len(g["graph"], g["name"], log_file_name)
        create_metrics_graph(all_log, g["graph"], log_file_name, g["name"])

        # except:
        #     print(g["name"], "でエラーが発生しました")
        #     continue

        # print("---------------------")


def create_metrics_graph(data_dict, graph, new_dir_path, name):
    diameter = nx.diameter(graph)
    chen_cell_size = (max(diameter, 2) + 1) / diameter

    x_idx = [x for x in data_dict.keys()]
    print(x_idx)
    metrics = [
        "stress",
        "edge_length_vaiance",
        "edge_crossings",
        "minimum_angle",
        "node_resolution",
    ]
    liner_dict = {
        "stress": [],
        "edge_length_vaiance": [],
        "edge_crossings": [],
        "minimum_angle": [],
        "node_resolution": [],
    }
    for x in x_idx:
        x_data = data_dict[x]
        n = len(x_data)
        for m in metrics:
            x_data_m = sorted([d[m] for d in x_data])
            liner_dict[m].append(x_data_m[n // 2])

    best_stress_comp = min(liner_dict["stress"])
    print("best_stress_comp", best_stress_comp)
    best_idx = liner_dict["stress"].index(best_stress_comp)
    print("best_idx", best_idx)
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


if __name__ == "__main__":
    main()
