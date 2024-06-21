import glob
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + "/")

import json
import os
import re

from matplotlib import pyplot as plt
import networkx as nx
from networkx.readwrite import json_graph


def save_graph(data, optimal_cell, chen_cell_size, dir_name, name, metrics):
    # 折れ線グラフの描画
    plt.figure(figsize=(10, 6))
    plt.plot([i * 0.05 for i in range(0, 80)], data)
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


"""
保存先
"""
new_dir_path = "metrics_networkx"
if not os.path.isdir(new_dir_path):
    os.mkdir(new_dir_path)
    os.mkdir(new_dir_path + "/metrics_liner")

folders = ["stress", "elv", "ec", "nr", "ma"]
for f in folders:
    path = new_dir_path + "/metrics_liner/" + f
    if not os.path.isdir(path):
        os.mkdir(path)

args = sys.argv
# ./test_liner_networkx_0617/log/
files = glob.glob(args[1] + "/*")

cell_size_files = glob.glob(args[1] + "/save_best_len_log/*")

graph_info = dict()

for filepath in cell_size_files:
    with open(filepath) as f:
        data = json.load(f)
    file_name = re.split("[/]", filepath)[-1][:-6]
    graph_info[file_name] = {"optimal_cell_size": data["best_multiple_num"]}


graph_files = glob.glob("./graphSet/networkx/*")
graphs = []
for filepath in graph_files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    file_name = re.split("[/]", filepath)[-1][:-5]
    graph_info[file_name]["graph"] = graph


for file in files:
    if os.path.isdir(file):
        continue

    # file = "./test_liner_networkx_0617/log/davis_southern_women-.json"
    name = re.split("[/-]", file)[-2]
    print(name)

    diameter = nx.diameter(graph_info[name]["graph"])
    chen_cell_size = (max(diameter, 2) + 1) / diameter

    with open(file) as f:
        data = json.load(f)

    liner_data = []
    for key in data.keys():
        d = data[key]
        if key != "file":
            liner_data.append([d["1"]["torusSGD"]])

    stress = [d[0]["stress"] for d in liner_data]
    elv = [d[0]["edge_length_vaiance"] for d in liner_data]
    ec = [d[0]["edge_crossings"] for d in liner_data]
    ma = [d[0]["minimum_angle"] for d in liner_data]
    nr = [d[0]["node_resolution"] for d in liner_data]

    save_graph(
        stress,
        graph_info[name]["optimal_cell_size"],
        chen_cell_size,
        new_dir_path,
        name,
        "stress",
    )
    save_graph(
        elv,
        graph_info[name]["optimal_cell_size"],
        chen_cell_size,
        new_dir_path,
        name,
        "elv",
    )
    save_graph(
        ec,
        graph_info[name]["optimal_cell_size"],
        chen_cell_size,
        new_dir_path,
        name,
        "ec",
    )
    save_graph(
        ma,
        graph_info[name]["optimal_cell_size"],
        chen_cell_size,
        new_dir_path,
        name,
        "ma",
    )
    save_graph(
        nr,
        graph_info[name]["optimal_cell_size"],
        chen_cell_size,
        new_dir_path,
        name,
        "nr",
    )
