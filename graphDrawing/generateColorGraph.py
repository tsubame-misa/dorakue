
import collections
import glob
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)+"/")
from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt
import networkx as nx
from common import log
import setup
import csv
import statistics
from algorithm.SGDBase import egraphSGD


"""
グラフの彩色数を取得する
"""


def generate_color_graph(graph, name, color):
    pos = egraphSGD.sgd(graph, name, 0)
    my_nx_other_param ={
        "node_color":color,
        "with_labels":True,
        "cmap":plt.cm.rainbow
    }
    nx.draw(graph, pos, **my_nx_other_param)
    plt.show()


def get_chromatic_number(graph, name):
    result =  nx.algorithms.coloring.greedy_color(graph)
    result_color = [ result.get(key) for key in graph.nodes]
    color_num = len(collections.Counter(result_color))
    # generate_color_graph(graph, name,  result_color)
    return color_num


def main():
    files = glob.glob("./graphSet/networkx/*")
    # files = glob.glob("./graphSet/doughNetGraph/default/*")
    # files = glob.glob("./graphSet/randomPartitionNetwork /*")
    # files = glob.glob("./graphSet/suiteSparse/*")


    with open("./graphSet/info2.json") as f:
        graph_info = json.load(f)

    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/]', filepath)[-1][:-5]
        obj = {"name": file_name, "graph": graph} #, "type":graph_info["Networkx"][file_name]["type"]}
        # obj = {"name": file_name, "graph": graph, "type":graph_info["Real world"][file_name]["type"]}
        # obj = {"name": file_name, "graph": graph, "type":graph_info["Random Partition2"][file_name]["type"]}
        # obj = {"name": file_name, "graph": graph, "type":graph_info["SuiteSparse Matrix"][file_name]["type"]}
        graphs.append(obj)


    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    log_file_name = "coloring_test"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        get_chromatic_number(g["graph"], g["name"])

if __name__ == '__main__':
    main()
