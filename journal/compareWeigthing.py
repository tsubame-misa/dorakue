import collections
import csv
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


class Weighting:
    def __init__(self, graph, size):
        self.graph = graph
        self.size = size

    def __call__(self, e):
        u, v = self.graph.edge_endpoints(e)
        u_set = set(self.graph.neighbors(u))
        v_set = set(self.graph.neighbors(v))
        return (len(u_set | v_set) - len(u_set & v_set)) / self.size


def get_avg_metrics(data):
    stress = []
    ec = []
    iel = []
    cam = []
    nr = []

    for d in data:
        stress.append(d["stress"])
        ec.append(d["edge_crossings"] + 1)
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

    # best_idx = stress.index(sorted_stress[n // 2])
    # obj = {
    #     "stress": data[best_idx]["stress"],
    #     "ec": data[best_idx]["edge_crossings"],
    #     "iel": data[best_idx]["ideal_edge_lengths"],
    #     "cam": data[best_idx]["crossing_angle_maximization"],
    #     "nr": data[best_idx]["node_resolution"],
    # }
    obj = {
        "stress": sorted_stress[n // 2],
        "ec": sorted_ec[n // 2],
        "iel": sorted_iel[n // 2],
        "cam": sorted_cam[n // 2],
        "nr": sorted_nr[n // 2],
    }
    return obj


def get_median_metrics(data, rename=False):
    stress = []
    ec = []
    iel = []
    cam = []
    nr = []

    if rename == "True":
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

    sorted_stress = sorted(stress)
    sorted_ec = sorted(ec)
    sorted_iel = sorted(iel)
    sorted_cam = sorted(cam)
    sorted_nr = sorted(nr)

    n = len(data)
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
        # if key == "iel":
        #     continue
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

    return obj


def download_csv(data):
    with open("weigthing_uniform.csv", mode="w", newline="") as file:
        # 辞書のキーをフィールド名として使用
        fieldnames = data[0].keys()  # ["name", "age", "city"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # ヘッダーを書き込み
        writer.writeheader()

        # データ行を書き込み
        writer.writerows(data)


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
            plt.axhline(y=1.1, color="blue")
            plt.show()

    # ボックスプロットの作成
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Key", y="Value", data=df_melted, showfliers=fliers, color="white")
    plt.title(title)
    plt.ylabel("rate (chen/optimal)")
    plt.axhline(y=1.0, color="blue", ls="--")
    # plt.axhline(y=0.9, color="blue")
    # plt.axhline(y=1.1, color="blue")
    plt.ylim(bottom=0)
    plt.show()


## これだと差が出ないのでダメ
def getCompareBoxPlot(data):
    filteredData = {
        "iel": {"normal": [], "weigthing": []},
        "cam": {"normal": [], "weigthing": []},
        "nr": {"normal": [], "weigthing": []},
    }

    for d in data.values():
        for edge_type in d.keys():
            if not (edge_type == "normal" or edge_type == "weigthing"):
                continue
            for metrics in d[edge_type].keys():
                if metrics in filteredData:
                    filteredData[metrics][edge_type].append(d[edge_type][metrics])
    print("filteredData", filteredData)
    # Create the box plots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    def getRange(data):
        allData = data["normal"] + data["weigthing"]
        print((min(allData), max(allData)))
        return (min(allData), max(allData))

    # Define y-limits for each category
    y_limits = {
        "iel": getRange(filteredData["iel"]),
        "cam": getRange(filteredData["cam"]),
        "nr": getRange(filteredData["nr"]),
    }

    # Plot for each category
    for category, values in filteredData.items():
        plt.figure(figsize=(6, 4))  # Create a new figure for each category
        data = []
        for key, value in values.items():
            for item in value:
                data.append([key, item])

        df = pd.DataFrame(data, columns=["Type", "Value"])

        sns.boxplot(
            x="Type",
            y="Value",
            data=df,
            palette={"normal": "red", "weigthing": "blue"},
            showfliers=False,
        )
        plt.title(f"Boxplot for {category}")
        # plt.ylim(y_limits[category])  # Set the y-axis limit based on the category

    plt.show()
    exit()


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

    with open("./graphSet0920/chen_weighting_cell_size_median.json") as f:
        chen_cell_size_info = json.load(f)

    graph_info = list2dict(_graph_info)
    results = {}

    chen_size_dict = {}
    csv_data = []

    for files_name in weighting_files:
        files = glob.glob(files_name)
        for file in files:
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-6]
            print(name)

            if not name in graph_info:
                continue

            if name in chen_cell_size_info:
                chen_cell_size = chen_cell_size_info[name]
            else:
                graph = eg.Graph()
                indices = {}
                for u in graph_dict[name].nodes:
                    indices[u] = graph.add_node(u)
                for u, v in graph_dict[name].edges:
                    graph.add_edge(indices[u], indices[v], (u, v))

                d = eg.all_sources_dijkstra(graph, Weighting(graph, 1))
                diameter = max(
                    d.get(u, v)
                    for u in graph.node_indices()
                    for v in graph.node_indices()
                )
                d_sum = sum(
                    [d.get(indices[u], indices[v]) for u, v in graph_dict[name].edges]
                )
                # どうとるかで結構変わる？変わらない？
                # 代表値
                # 最頻値・
                # d_avg = d_sum / len(graph_dict[name].edges)
                sorted_edge = sorted(
                    [d.get(indices[u], indices[v]) for u, v in graph_dict[name].edges]
                )
                d_median = sorted_edge[len(graph_dict[name].edges) // 2]
                chen_cell_size = (max(diameter, 2) + d_median) / diameter
                # chen_cell_size = "1.0"  # , int(chen_cell_size * 100) // 100
                digit2 = ((chen_cell_size * 10) // 1) / 10
                # print(digit2)
                chen_cell_size = ((chen_cell_size * 100) // 1) / 100
                # print(chen_cell_size)

                if not (str(chen_cell_size) in data["data"]):
                    diff = chen_cell_size - digit2
                    if diff < 0.03:
                        chen_cell_size = digit2
                    elif diff < 0.07:
                        chen_cell_size = digit2 + 0.05
                    else:
                        chen_cell_size = digit2 + 0.1
                    chen_cell_size = ((chen_cell_size * 100) // 1) / 100
                    # print("re", chen_cell_size)

                print("chen_cell_size", chen_cell_size)

            chen_size_dict[name] = chen_cell_size

            # weigthing_res = get_avg_metrics(data["data"][str(chen_cell_size)])
            weigthing_res = get_median_data_metrics(data["data"][str(chen_cell_size)])
            results[name] = {}
            results[name]["weigthing"] = weigthing_res
            results[name]["type"] = graph_info[name]["type"]

    print(chen_size_dict)

    for files_name in normal_files:
        files = glob.glob(files_name)
        for file in files:
            if not os.path.isfile(file):
                continue
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-6]
            if not name in chen_size_dict:
                continue
            print(name)
            if str(chen_size_dict[name]) in data:
                print("beforeData", name)
                res = get_metrics(
                    data[str(chen_size_dict[name])]["1"]["torusSGD"],
                    graph_dict[name],
                )
            else:
                # TODO:こっちでやる
                # res = get_avg_metrics(
                #     data["data"][str(chen_size_dict[name])]
                # )
                res = get_median_data_metrics(data["data"][str(chen_size_dict[name])])
            results[name]["normal"] = res
            rate_res = get_rate(
                results[name]["normal"],
                results[name]["weigthing"],
                name,
                results[name]["type"],
            )
            results[name]["rate"] = rate_res
            # csv_obj = rate_res
            # csv_obj["name"] = name
            # csv_obj["weigthed"] = chen_size_dict[name]
            # csv_obj["uniform"] = chen_cell_size
            # csv_obj["type"] = graph_info[name]["type"]
            # csv_data.append(csv_obj)

    # download_csv(csv_data)

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
