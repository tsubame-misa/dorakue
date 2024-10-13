import collections
import glob
import math
import re
import sys
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import egraph as eg
import networkx as nx

sys.path.append(str(Path(__file__).parent.parent) + "/")

from networkx.readwrite import json_graph
import json


"""
最適なセルサイズでの描画は、美的指標が良くなる←最適なセルサイズでの描画結果を、chenと比較
rateでの比較ではなく、箱ヒゲのプロットで
"""


class Weighting:
    def __init__(self, graph, size):
        self.graph = graph
        self.size = size

    def __call__(self, e):
        u, v = self.graph.edge_endpoints(e)
        u_set = set(self.graph.neighbors(u))
        v_set = set(self.graph.neighbors(v))
        return (len(u_set | v_set) - len(u_set & v_set)) / self.size


def get_avg_metrics(data, rename=False):
    stress = []
    ec = []
    iel = []
    cam = []
    nr = []

    if rename == "True" or rename == True:
        for d in data:
            stress.append(d["stress"])
            ec.append(d["edge_crossings"])
            iel.append(d["ideal_edge_lengths"])
            cam.append(d["crossing_angle_maximization"])
            nr.append(d["node_resolution"])
    else:
        for d in data:
            stress.append(d["stress"])
            ec.append(d["edge_crossings"])
            iel.append(d["edge_length_vaiance"])
            cam.append(d["minimum_angle"])
            nr.append(d["node_resolution"])

    n = len(data)
    obj = {
        "stress": sum(stress) / n,
        "edge_crossings": sum(ec) / n,
        "ideal_edge_lengths": sum(iel) / n,
        "crossing_angle_maximization": sum(cam) / n,
        "node_resolution": sum(nr) / n,
    }
    return obj


def show_box_plot(data, title, detail=False):
    flat_data = []
    for d in data:
        print(d)
        if "chen" in d:
            flat_data.append(d["chen"])
        if "optimal" in d:
            flat_data.append(d["optimal"])

    print(flat_data)
    # データフレームの作成
    df = pd.DataFrame(flat_data)

    # print(df)

    # データを長い形式に変換
    # df_melted = df.melt(var_name="Key", value_name="Value")

    palette = {"chen": "orange", "optimal": "green"}
    print(df.columns)

    for c_name in df.columns:
        df_c = df[c_name]
        print(c_name)
        # ボックスプロットの作成
        plt.figure(figsize=(10, 6))
        sns.boxplot(x="method", y=c_name, data=df, showfliers=False, palette=palette)
        plt.title(title + " " + c_name)
        plt.ylabel("value")
        # plt.axhline(y=1.0, color="red")
        # plt.axhline(y=0.9, color="blue")
        plt.show()

    # ボックスプロットの作成
    # plt.figure(figsize=(10, 6))
    # sns.boxplot(x="Key", y="Value", data=df_melted, showfliers=False)
    # plt.title(title)
    # plt.ylabel("rate (chen/optimal)")
    # plt.axhline(y=1.0, color="red")
    # plt.axhline(y=0.9, color="blue")
    # plt.show()


def list2dict(data):
    data_dict = {}
    for d in data:
        data_dict.update(d)
    return data_dict


"""
chen_files, optimal_files, renamed_optimal_file = True/False, weigthing_optimal = True/False

python3 journal/compareChenOptimal.py ./journal/data/chen/chen_torus_cell_size_networkx/log ./optimal_weigthing_networkx_0625/log True

chen_files = [
    "./journal/data/chen/chen_torus_cell_size_networkx/log/*",
    "./journal/data/chen/chen_torus_cell_size_dough/log/*",
    "./journal/data/chen/chen_torus_cell_size_random/log/*",
    "./journal/data/chen/chen_torus_cell_size_sparse/log/*",
    "./journal/data/chen/chen_networkx_50/log/*",
]
optimal_files = [
    "./journal/data/optimal/optimal_torus_cell_size_networkx/log/*",
    "./journal/data/optimal/optimal_torus_cell_size_dough/log/*",
    "./journal/data/optimal/optimal_torus_cell_size_random/log/*",
    "./journal/data/optimal/optimal_torus_cell_size_sparse/log/*",
    "./journal/data/optimal/optimal_networkx_50/log/*",
]
"""


def main():
    args = sys.argv
    print(args)
    chen_files = glob.glob(args[0] + "/*")
    optimal_files = glob.glob(args[1] + "/*")
    chen_files = [
        # "./journal/data/chen/chen_torus_cell_size_networkx/log/*",
        # "./journal/data/chen/chen_torus_cell_size_dough/log/*",
        "./journal/data/chen/chen_torus_cell_size_random/log/*",
        # "./journal/data/chen/chen_torus_cell_size_sparse/log/*",
        # "./journal/data/chen/chen_networkx_50/log/*",
    ]
    optimal_files = [
        # "./optimal_weigthing_networkx_0625/log/*",
        # "./optimal_weigthing_dough_0625/log/*",
        "./optimal_weigthing_random/log/*",
        # "./optimal_weigthing_sparse/log/*",
    ]

    renamed_optimal_file = args[2]
    print("renamed_optimal_file", renamed_optimal_file)

    graph_files = [
        "./graphSet/networkx/*",
        "./graphSet/doughNetGraph/default/*",
        "./graphSet/randomPartitionNetwork /*",
        "./graphSet/suiteSparse/*",
    ]

    graph_dict = {}
    for gf in graph_files:
        files = glob.glob(gf)
        for f in files:
            graph = json_graph.node_link_graph(json.load(open(f)))
            file_name = re.split("[/]", f)[-1][:-5]
            graph_dict[file_name] = graph

    with open("./graphSet/info202405_egraph.json") as f:
        # _graph_info = json.load(f)
        _graph_info = [g for g in json.load(f).values()]

    graph_info = list2dict(_graph_info)

    results = dict()
    for files_name in chen_files:
        files = glob.glob(files_name)
        for file in files:
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-10]
            res = get_avg_metrics(data)
            res["method"] = "chen"
            results[name] = dict()
            results[name]["chen"] = res
            results[name]["type"] = graph_info[name]["type"]

    for files_name in optimal_files:
        files = glob.glob(files_name)
        for file in files:
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-10]
            print("name", name)
            res["method"] = "optimal"
            res = get_avg_metrics(
                data,
                renamed_optimal_file,
            )
            results[name]["optimal"] = res

    """
    比率での比較結果
    """

    types = [d["type"] for d in results.values()]
    c = collections.Counter(types)
    print(c)
    type_a_rate_data = [
        d for d in list(filter(lambda x: x["type"] == "a", results.values()))
    ]

    show_box_plot(type_a_rate_data, "a")

    type_b_rate_data = [
        d
        for d in list(
            filter(lambda x: x["type"] == "b" or x["type"] == "c", results.values())
        )
    ]
    show_box_plot(type_b_rate_data, "b or c")

    type_b_rate_data = [d for d in results.values()]
    # show_box_plot(type_b_rate_data, "all")

    exit()

    """
    平均値での比較
    """
    type_a_chen_data = [
        d["chen"] for d in list(filter(lambda x: x["type"] == "a", results.values()))
    ]
    type_a_optimal_data = [
        d["optimal"]
        for d in list(filter(lambda x: x["type"] == "a", results.values()))
        if "optimal" in d
    ]
    print("chen a", get_avg_metrics(type_a_chen_data, rename=True))
    print("optimal a", get_avg_metrics(type_a_optimal_data, rename=True))

    type_b_chen_data = [
        d["chen"]
        for d in list(
            filter(lambda x: x["type"] == "b" or x["type"] == "c", results.values())
        )
    ]

    type_b_optimal_data = [
        d["optimal"]
        for d in list(
            filter(lambda x: x["type"] == "b" or x["type"] == "c", results.values())
        )
        if "optimal" in d
    ]

    print("chen b", get_avg_metrics(type_b_chen_data, rename=True))
    print("optimal b", get_avg_metrics(type_b_optimal_data, rename=True))


if __name__ == "__main__":
    main()
