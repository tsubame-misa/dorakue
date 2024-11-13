import collections
import glob
import math
import os
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
"""


def get_avg_metrics(data, graph, rename=False, weigthing=False):
    stress = []
    ec = []
    iel = []
    cam = []
    nr = []
    elv = []
    gp = []
    np = []
    ma = []

    # print(data)
    # exit()

    for d in data:
        stress.append(d["stress"])
        ec.append(d["edge_crossings"])
        iel.append(d["ideal_edge_lengths"])
        cam.append(d["crossing_angle_maximization"])
        nr.append(d["node_resolution"])

    n = len(data)
    obj = {
        "stress": sum(stress) / n,
        "ec": sum(ec) / n,
        "iel": sum(iel) / n,
        "cam": sum(cam) / n,
        "nr": sum(nr) / n,
        # "gp": sum(gp) / n,
        # "np": sum(np) / n,
        # "elv": sum(elv) / n,
    }
    return obj


def get_median_data_metrics(data):
    stress = []
    n = len(data)
    for d in data:
        stress.append(d["stress"])

    sorted_stress = sorted(stress)
    best_idx = stress.index(sorted_stress[n // 2])

    obj = {
        "stress": data[best_idx]["stress"],
        "ec": data[best_idx]["edge_crossings"],
        "iel": data[best_idx]["ideal_edge_lengths"],
        "cam": data[best_idx]["crossing_angle_maximization"],
        "nr": data[best_idx]["node_resolution"],
    }
    return obj


def get_median_data_metrics(data):
    stress = []
    ec = []
    iel = []
    cam = []
    nr = []
    n = len(data)
    for d in data:
        stress.append(d["stress"])
        ec.append(d["edge_crossings"])
        iel.append(d["ideal_edge_lengths"])
        cam.append(d["crossing_angle_maximization"])
        nr.append(d["node_resolution"])

    sorted_stress = sorted(stress)
    sorted_ec = sorted(ec)
    sorted_iel = sorted(iel)
    sorted_cam = sorted(cam)
    sorted_nr = sorted(nr)

    obj = {
        "stress": sorted_stress[n // 2],
        "ec": sorted_ec[n // 2],
        "iel": sorted_iel[n // 2],
        "cam": sorted_cam[n // 2],
        "nr": sorted_nr[n // 2],
    }
    return obj


def get_metrics(data, graph):
    obj = {
        "stress": data["stress"],
        "ec": data["edge_crossings"],
        "iel": -10,
        "cam": data["minimum_angle"],
        "nr": data["node_resolution"],
    }
    return obj


def get_rate(chen, optimal, name="name", _type="-"):
    obj = dict()
    flg = False
    for key in chen.keys():
        if optimal[key] == 0:
            if chen[key] == 0:
                obj[key] = 1
            # ※ 比で表してるのが良くなかったりする？
            elif key == "ec":
                obj[key] = (chen[key] + 1) / 1
            else:
                # ここどうするべき？
                obj[key] = 1.5
                # obj[key] = 10 * chen[key]
        else:
            obj[key] = chen[key] / optimal[key]
        # if key == "elv":
        #     print(name, chen[key] / optimal[key], chen[key], optimal[key])

        # if key == "minimum_angle" and _type != "a" and obj[key] < 0.8:
        #     flg = True
        #     print("|", name, "|", obj[key], "|", chen[key], "|", optimal[key], "|")

        if obj[key] < 0.9:
            print(name, key, obj[key], chen[key], optimal[key])

    if flg:
        print(name, _type, obj)
        print("------------------")

    ## CSV
    # print(
    #     name,
    #     ",",
    #     _type,
    #     ",",
    #     obj["stress"],
    #     ",",
    #     obj["edge_crossings"],
    #     ",",
    #     obj["ideal_edge_lengths"],
    #     ",",
    #     obj["crossing_angle_maximization"],
    #     ",",
    #     obj["node_resolution"],
    #     ",",
    #     obj["gp"],
    #     # ",",
    #     # obj["np"],
    # )
    return obj


def show_box_plot(data, title, detail=False, fliers=False):
    # データフレームの作成
    df = pd.DataFrame(data)

    # データを長い形式に変換
    df_melted = df.melt(var_name="Key", value_name="Value")

    if detail:
        for c_name in df.columns:
            df_c = df[c_name]
            # ボックスプロットの作成
            plt.figure(figsize=(10, 6))
            sns.boxplot(df_c, showfliers=fliers)
            plt.title(title + " " + c_name)
            plt.ylabel("rate (chen/optimal)")
            plt.axhline(y=1.0, color="red")
            plt.axhline(y=0.9, color="blue")
            plt.show()

    # ボックスプロットの作成
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Key", y="Value", data=df_melted, color="white", showfliers=fliers)
    plt.title(title)
    plt.ylabel("rate (chen/optimal)")
    plt.axhline(y=1.0, color="blue", ls="--")
    plt.axhline(y=0, color="white", ls="--")
    # plt.axhline(y=0.9, color="blue")
    plt.show()


def list2dict(data):
    data_dict = {}
    for d in data:
        data_dict.update(d)
    return data_dict


def main():
    normal_files = [f + "/log/*" for f in glob.glob("./journal/data/liner/*")]
    weighting_files = [
        f + "/log/*" for f in glob.glob("./journal/data/weigthing_liner/*")
    ]
    graph_files = [f + "/*" for f in glob.glob("./graphSet0920/*")]

    graph_dict = {}
    for gf in graph_files:
        files = glob.glob(gf)
        for f in files:
            graph = json_graph.node_link_graph(json.load(open(f)))
            file_name = re.split("[/]", f)[-1][:-5]
            graph_dict[file_name] = graph

    with open("./graphSet0920/info_weigthed.json") as f:
        _graph_info = [g for g in json.load(f).values()]

    graph_info = list2dict(_graph_info)
    results = {}

    optimal_size_dict = {}

    for files_name in weighting_files:
        files = glob.glob(files_name)
        for file in files:
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-6]
            print(name)

            if not name in graph_info:
                continue

            optimal_size = data["optimal_cell_size"]

            optimal_size_dict[name] = optimal_size

            weigthing_res = get_median_data_metrics(
                data["data"][str(optimal_size)],
            )
            results[name] = {}
            results[name]["weigthing"] = weigthing_res
            results[name]["type"] = graph_info[name]["type"]

    print(optimal_size)

    for files_name in normal_files:
        files = glob.glob(files_name)
        for file in files:
            if not os.path.isfile(file):
                continue
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-6]

            print(name)
            # TODO:こっちでやる
            optimal_size = data["optimal_cell_size"]
            print(name, "normal", optimal_size)
            res = get_median_data_metrics(
                data["data"][str(optimal_size)],
            )

            if not name in results:
                continue
            results[name]["normal"] = res
            rate_res = get_rate(
                results[name]["normal"],
                results[name]["weigthing"],
                name,
                results[name]["type"],
            )
            results[name]["rate"] = rate_res

    """
    比率での比較結果
    """
    _results = {}
    for key in results.keys():
        if "rate" in results[key]:
            _results[key] = results[key]

    types = [d["type"] for d in results.values()]
    c = collections.Counter(types)
    print(c)

    type_a_rate_data = [
        d["rate"]
        for d in list(filter(lambda x: x["type"] == "a", _results.values()))
        if d["rate"]["stress"] > 0.9
    ]

    show_box_plot(type_a_rate_data, "a")

    type_b_rate_data = [
        d["rate"]
        for d in list(
            filter(lambda x: x["type"] == "b" or x["type"] == "c", _results.values())
        )
        if d["rate"]["stress"] > 0.9
    ]
    show_box_plot(type_b_rate_data, "b or c")

    type_b_rate_data = [
        d["rate"] for d in _results.values() if d["rate"]["stress"] > 0.9
    ]
    # show_box_plot(type_b_rate_data, "all", True, True)
    show_box_plot(type_b_rate_data, "all")


if __name__ == "__main__":
    main()
