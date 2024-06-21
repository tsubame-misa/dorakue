import collections
import glob
import math
import re
import sys
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

import networkx as nx

sys.path.append(str(Path(__file__).parent.parent) + "/")

from networkx.readwrite import json_graph
import json


"""
最適なセルサイズでの描画は、美的指標が良くなる←最適なセルサイズでの描画結果を、chenと比較
"""


def calc_gabiel_property(pos, graph):
    gp = 0
    for i, j in graph.edges:
        for v in graph.nodes:
            if i == v or j == v:
                continue
            pos_i = pos[str(i)]
            pos_j = pos[str(j)]
            pos_v = pos[str(v)]
            r_ij = math.hypot(pos_i[0] - pos_j[0], pos_i[1] - pos_j[1]) / 2
            c_ij = [(pos_i[0] + pos_j[0]) / 2, (pos_i[1] + pos_j[1]) / 2]
            d = r_ij - math.hypot(pos_v[0] - c_ij[0], pos_v[1] - c_ij[1])
            if d > 0:
                # 円の内側にノードがあるのでペナルティ
                gp += max(0, d**2)
            # gp += max(0, d**2)

    return gp


def neighborhood_preservation(pos, graph):
    dist = [[[float("inf"), i] for i in range(len(pos))] for j in range(len(pos))]
    node_name = [str(k) for k in graph.nodes.keys()]
    for i in range(len(pos) - 1):
        for j in range(i + 1, len(pos)):
            pos_i = pos[node_name[i]]
            pos_j = pos[node_name[j]]
            d = math.hypot(pos_i[0] - pos_j[0], pos_i[1] - pos_j[1])
            dist[i][j][0] = d
            dist[j][i][0] = d

    np = 0
    for v in graph.nodes:
        v_index = node_name.index(str(v))
        degree = graph.degree(v)
        sorted_d = sorted(dist[v_index], key=lambda x: x[0])
        knn = set([i for value, i in sorted_d[:degree]])
        rinsetu = set(nx.all_neighbors(graph, v))
        jaccard = len(knn & rinsetu) / len(knn | rinsetu)

        np += jaccard
    np /= len(graph.nodes)
    return np


def get_avg_metrics(data, graph):

    stress = []
    ec = []
    elv = []
    ma = []
    nr = []
    gp = []
    np = []

    for d in data:
        # _np = neighborhood_preservation(d["pos"], graph)
        # np.append(_np)
        _gp = calc_gabiel_property(d["pos"], graph)
        gp.append(_gp)
        stress.append(d["stress"])
        ec.append(d["edge_crossings"])
        elv.append(d["edge_length_vaiance"])
        ma.append(d["minimum_angle"])
        nr.append(d["node_resolution"])

    n = len(data)
    obj = {
        "stress": sum(stress) / n,
        "edge_crossings": sum(ec) / n,
        "edge_length_vaiance": sum(elv) / n,
        "minimum_angle": sum(ma) / n,
        "node_resolution": sum(nr) / n,
        "gp": sum(gp) / n,
        # "np": sum(np) / n,
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
        "edge_crossings": data[best_idx]["edge_crossings"],
        "edge_length_vaiance": data[best_idx]["edge_length_vaiance"],
        "minimum_angle": data[best_idx]["minimum_angle"],
        "node_resolution": data[best_idx]["node_resolution"],
    }
    return obj


def get_median_metrics(data):
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

    sorted_stress = sorted(stress)
    sorted_ec = sorted(ec)
    sorted_elv = sorted(elv)
    sorted_ma = sorted(ma)
    sorted_nr = sorted(nr)

    n = len(data)
    obj = {
        "stress": sorted_stress[n // 2],
        "edge_crossings": sorted_ec[n // 2],
        "edge_length_vaiance": sorted_elv[n // 2],
        "minimum_angle": sorted_ma[n // 2],
        "node_resolution": sorted_nr[n // 2],
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
            elif key == "edge_crossings":
                obj[key] = (chen[key] + 1) / 1
            else:
                # ここどうするべき？
                obj[key] = 1.5
                # obj[key] = 10 * chen[key]
        else:
            obj[key] = chen[key] / optimal[key]

        # if key == "minimum_angle" and _type != "a" and obj[key] < 0.8:
        #     flg = True
        #     print("|", name, "|", obj[key], "|", chen[key], "|", optimal[key], "|")

        # if obj[key] < 0.8:
        #     flg = True
        # print(name, key, obj[key], chen[key], optimal[key])

    if flg:
        print(name, _type, obj)
        print("------------------")
    print(
        name,
        ",",
        _type,
        ",",
        obj["stress"],
        ",",
        obj["edge_crossings"],
        ",",
        obj["edge_length_vaiance"],
        ",",
        obj["minimum_angle"],
        ",",
        obj["node_resolution"],
        ",",
        obj["gp"],
        # ",",
        # obj["np"],
    )
    return obj


def show_box_plot(data, title):
    # データフレームの作成
    df = pd.DataFrame(data)

    # データを長い形式に変換
    df_melted = df.melt(var_name="Key", value_name="Value")

    # for c_name in df.columns:
    #     df_c = df[c_name]
    #     # ボックスプロットの作成
    #     plt.figure(figsize=(10, 6))
    #     sns.boxplot(df_c, showfliers=False)
    #     plt.title(title + " " + c_name)
    #     plt.ylabel("rate (chen/optimal)")
    #     plt.axhline(y=1.0, color="red")
    #     plt.axhline(y=0.9, color="blue")
    #     plt.show()

    # ボックスプロットの作成
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="Key", y="Value", data=df_melted, showfliers=False)
    plt.title(title)
    plt.ylabel("rate (chen/optimal)")
    plt.axhline(y=1.0, color="red")
    plt.axhline(y=0.9, color="blue")
    plt.show()


def list2dict(data):
    data_dict = {}
    for d in data:
        data_dict.update(d)
    return data_dict


def main():
    chen_files = [
        # "./journal/data/chen/chen_torus_cell_size_networkx/log/*",
        # "./journal/data/chen/chen_torus_cell_size_dough/log/*",
        # "./journal/data/chen/chen_torus_cell_size_random/log/*",
        # "./journal/data/chen/chen_torus_cell_size_sparse/log/*",
        "./journal/data/chen/chen_networkx_50/log/*",
    ]
    optimal_files = [
        # "./journal/data/optimal/optimal_torus_cell_size_networkx/log/*",
        # "./journal/data/optimal/optimal_torus_cell_size_dough/log/*",
        # "./journal/data/optimal/optimal_torus_cell_size_random/log/*",
        # "./journal/data/optimal/optimal_torus_cell_size_sparse/log/*",
        "./journal/data/optimal/optimal_networkx_50/log/*",
    ]

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
            res = get_avg_metrics(data, graph_dict[name])
            res_median = get_median_metrics(data)
            results[name] = dict()
            results[name]["chen"] = res
            results[name]["chen_median"] = res_median
            results[name]["type"] = graph_info[name]["type"]

    for files_name in optimal_files:
        files = glob.glob(files_name)
        for file in files:
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-10]
            res = get_avg_metrics(data, graph_dict[name])
            res_median = get_median_metrics(data)
            results[name]["optimal"] = res
            results[name]["optimal_median"] = res_median
            rate_res = get_rate(
                results[name]["chen"],
                results[name]["optimal"],
                name,
                results[name]["type"],
            )
            results[name]["rate"] = rate_res
            # rate_res_median = get_rate(
            #     results[name]["chen_median"],
            #     results[name]["optimal_median"],
            #     name,
            #     results[name]["type"],
            # )
            # results[name]["rate"] = rate_res_median
            # if results[name]["rate"]["stress"] <= 0.95:
            #     print("stress is bad", name, results[name]["type"])

    """
    比率での比較結果
    """
    types = [d["type"] for d in results.values()]
    c = collections.Counter(types)
    print(c)

    type_a_rate_data = [
        d["rate"] for d in list(filter(lambda x: x["type"] == "a", results.values()))
    ]

    show_box_plot(type_a_rate_data, "a")

    type_b_rate_data = [
        d["rate"]
        for d in list(
            filter(lambda x: x["type"] == "b" or x["type"] == "c", results.values())
        )
    ]
    show_box_plot(type_b_rate_data, "b or c")

    exit()

    """
    平均値での比較
    """
    type_a_chen_data = [
        d["chen"] for d in list(filter(lambda x: x["type"] == "a", results.values()))
    ]
    type_a_optimal_data = [
        d["optimal"] for d in list(filter(lambda x: x["type"] == "a", results.values()))
    ]
    print("chen a", get_avg_metrics(type_a_chen_data))
    print("optimal a", get_avg_metrics(type_a_optimal_data))

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
    ]

    print("chen a", get_avg_metrics(type_b_chen_data))
    print("optimal a", get_avg_metrics(type_b_optimal_data))


if __name__ == "__main__":
    main()
