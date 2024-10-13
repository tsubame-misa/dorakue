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


def list2dict(data):
    data_dict = {}
    for d in data:
        data_dict.update(d)
    return data_dict


def main():
    files = {
        "./graphSet0920/networkx/*",
        "./graphSet0920/doughNetGraph/default/*",
        "./graphSet0920/doughNetGraph0920/*",
        "./graphSet0920/randomPartitionNetwork/*",
        "./graphSet0920/randomPartitionNetwork0920/*",
        "./graphSet0920/suiteSparse/*",
        "./graphSet0920/suiteSparse0920/*",
    }

    with open("./graphSet0920/info_weigthed.json") as f:
        _graph_info = [g for g in json.load(f).values()]
    graph_info = list2dict(_graph_info)

    graph_dict = {}

    for gf in files:
        files = glob.glob(gf)
        for f in files:
            file_name = re.split("[/]", f)[-1][:-5]
            if not file_name in graph_info:
                continue

            graph = json_graph.node_link_graph(json.load(open(f)))
            graph_dict[file_name] = graph

    data = [[len(g.nodes), len(g.edges)] for g in graph_dict.values()]
    sorted_data = sorted(data, key=lambda x: x[0])
    print(sorted_data, len(data))

    cnt = 0
    for d in data:
        if d[0] <= 106:
            cnt += 1

    print(cnt, len(data))
    exit()

    # Extracting the X and Y values

    x_values = [item[0] for item in data]
    y_values = [item[1] for item in data]

    # Creating the scatter plot
    plt.scatter(x_values, y_values)

    # Adding labels and title
    plt.xlabel("node values")
    plt.ylabel("edge values")
    plt.title("Scatter Plot of Provided Data")

    # Display the plot
    plt.show()


if __name__ == "__main__":
    main()
