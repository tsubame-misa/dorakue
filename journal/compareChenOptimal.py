import collections
import glob
import re
import sys
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent) + "/")

from networkx.readwrite import json_graph
import json


"""
最適なセルサイズでの描画は、美的指標が良くなる←最適なセルサイズでの描画結果を、chenと比較
"""


def get_avg_metrics(data):
    stress = []
    ec = []
    elv = []
    ma = []
    nr = []

    for d in data:
        stress.append(d["stress"])
        ec.append(d["edge_crossings"])
        elv.append(d["edge_length_vaiance"])
        ma.append(d["minimum_angle"])
        nr.append(d["node_resolution"])

    n = len(data)
    return {
        "stress": sum(stress) / n,
        "ec": sum(ec) / n,
        "elv": sum(elv) / n,
        "ma": sum(ma) / n,
        "nr": sum(nr) / n,
    }


def get_rate(chen, optimal):
    obj = dict()
    for key in chen.keys():
        if optimal[key] == 0:
            obj[key] = 0
        else:
            obj[key] = chen[key] / optimal[key]
    return obj


def show_box_plot(data, title):
    # データフレームの作成
    df = pd.DataFrame(data)

    # データを長い形式に変換
    df_melted = df.melt(var_name="Key", value_name="Value")

    # ボックスプロットの作成
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Key", y="Value", data=df_melted, showfliers=False)
    plt.title(title)
    plt.ylabel("rate (chen/optimal)")
    plt.axhline(y=1.0, color="red")
    plt.show()


def list2dict(data):
    print("----------")
    print(len(data))
    data_dict = {}
    for d in data:
        data_dict.update(d)
    print("return", len(data_dict))
    return data_dict


def main():
    chen_files = [
        "./journal/data/chen/chen_torus_cell_size_networkx/log/*",
        "./journal/data/chen/chen_torus_cell_size_dough/log/*",
        "./journal/data/chen/chen_torus_cell_size_random/log/*",
        "./journal/data/chen/chen_torus_cell_size_sparse/log/*",
    ]
    optimal_files = [
        "./journal/data/optimal/optimal_torus_cell_size_networkx/log/*",
        "./journal/data/optimal/optimal_torus_cell_size_dough/log/*",
        "./journal/data/optimal/optimal_torus_cell_size_random/log/*",
        "./journal/data/optimal/optimal_torus_cell_size_sparse/log/*",
    ]

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
            results[name] = dict()
            results[name]["chen"] = res
            results[name]["type"] = graph_info[name]["type"]

    for files_name in optimal_files:
        files = glob.glob(files_name)
        for file in files:
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-10]
            res = get_avg_metrics(data)
            results[name]["optimal"] = res
            rate_res = get_rate(results[name]["chen"], results[name]["optimal"])
            results[name]["rate"] = rate_res
            if results[name]["type"] == "b" or results[name]["type"] == "c":
                if results[name]["rate"]["stress"] <= 0.95:
                    print(name)

    type_a_rate_data = [
        d["rate"] for d in list(filter(lambda x: x["type"] == "a", results.values()))
    ]

    # show_box_plot(type_a_rate_data, "a")

    type_b_rate_data = [
        d["rate"]
        for d in list(
            filter(lambda x: x["type"] == "b" or x["type"] == "c", results.values())
        )
    ]
    # show_box_plot(type_b_rate_data, "b or c")

    types = [d["type"] for d in results.values()]
    # print(types)
    c = collections.Counter(types)
    print(c)


if __name__ == "__main__":
    main()
