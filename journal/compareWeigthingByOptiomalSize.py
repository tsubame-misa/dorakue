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


class Weighting:
    def __init__(self, graph, size):
        self.graph = graph
        self.size = size

    def __call__(self, e):
        u, v = self.graph.edge_endpoints(e)
        u_set = set(self.graph.neighbors(u))
        v_set = set(self.graph.neighbors(v))
        return (len(u_set | v_set) - len(u_set & v_set)) / self.size


def torus_dist(u, v, size):
    x_list = [v[0] - size, v[0], v[0] + size]
    y_list = [v[1] - size, v[1], v[1] + size]

    best_pos = [v[0], v[1]]
    _dist = float("inf")

    for x in x_list:
        for y in y_list:
            ax = u[0] - x
            ay = u[1] - y
            adist = (ax**2 + ay**2) ** 0.5
            if _dist > adist:
                best_pos[0] = ax
                best_pos[1] = ay
                _dist = adist

    return _dist


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


def calc_edge_length_variance(pos, original_graph, multiple_num, weigthing=False):
    graph = eg.Graph()
    indices = {}
    for u in original_graph.nodes:
        indices[u] = graph.add_node(u)
    for u, v in original_graph.edges:
        graph.add_edge(indices[u], indices[v], (u, v))

    if weigthing:
        d = eg.all_sources_dijkstra(graph, Weighting(graph, 1))
    else:
        d = eg.all_sources_dijkstra(graph, lambda _: 1)

    diameter = max(
        d.get(u, v) for u in graph.node_indices() for v in graph.node_indices()
    )

    size = diameter * multiple_num

    dist_array = []
    for i, j in original_graph.edges:
        pos_i = pos[str(i)]
        pos_j = pos[str(j)]
        # torus なら torus上の距離でやらないといけない
        d = torus_dist(pos_i, pos_j, size)
        # d = math.hypot(pos_i[0] - pos_j[0], pos_i[1] - pos_j[1])
        dist_array.append(d)
    d_avg = sum(dist_array) / len(original_graph.edges)
    elv = 0
    for d in dist_array:
        elv += (d - d_avg) ** 2
    return elv / (len(original_graph.edges))


def calc_minimum_angle(pos, graph):
    # for v in graph.nodes:
    #     neighbors = nx.all_neighbors(graph, v)
    # print(neighbors)
    # ideal_theta = 360 / len(neighbors)
    # exit()
    return


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
        # _np = neighborhood_preservation(d["pos"], graph)
        # np.append(_np)
        # _gp = calc_gabiel_property(d["pos"], graph)
        # gp.append(_gp)
        # _elv = calc_edge_length_variance(
        #     d["pos"], graph, d["multiple_num"], weigthing
        # )
        # elv.append(_elv)
        # _ma = calc_minimum_angle(d["pos"], graph)
        # ma.append(_ma)
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
    # optimal_liner_files = glob.glob(args[1] + "/*")

    # TODO: 平均データでやる(現状1つ)
    # TODO: 平均データでやる(現状5つ)
    normal_files = [
        "./journal/data/liner/networkx_5/log/*",
        "./journal/data/liner/liner_dough_5/log/*",
        "./journal/data/liner/liner_random_5/log/*",
        "./liner_sparse5/log/*",
        # "./graphDrawing/data/egraph/liner_egraph_networkx_20/log/*",
        # "./graphDrawing/data/egraph/liner_egraph_dough_20/log/*",
        # "./graphDrawing/data/egraph/liner_egraph_random_20/log/*",
        # "./graphDrawing/data/egraph/liner_egraph_sparse_20/log/*",
    ]
    weighting_files = [
        "./journal/data/weigthing_liner/networkx/log/*",
        "./journal/data/weigthing_liner/douh/log/*",
        "./journal/data/weigthing_liner/random/log/*",
        "./test_liner_weighting_sparse/log/*",
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
    results = {}

    optimal_size_dict = {}

    for files_name in weighting_files:
        files = glob.glob(files_name)
        for file in files:
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-6]
            print(name)

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
