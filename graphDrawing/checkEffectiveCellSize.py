"""
ストレス許容誤差を調べる
+-1.5 でストレスが最小値の何倍になるかをboxplotで表示
+-0.75くらいで切りたい気持ちがあるが...
"""

import glob
import json
import math
import os
import re
from functools import reduce
import matplotlib.pyplot as plt
import seaborn as sns


def list2dict(data):
    data_dict = {}
    for d in data:
        data_dict.update(d)
    return data_dict


def get_metrics_raito(_data, metrics_name):
    data = _data["data"]
    optimal_cell_size = _data["optimal_cell_size"]
    optimal_metrics = sorted([d[metrics_name] for d in data[str(optimal_cell_size)]])
    min_stress = optimal_metrics[len(optimal_metrics) // 2]

    x = [n for n in data.keys()]
    y = []
    diff_x = []

    for n in x:
        if abs(optimal_cell_size - float(n)) > 0.2:
            continue
        metrics = sorted([d[metrics_name] for d in data[n]])
        if min_stress == 0:
            if metrics_name == "edge_crossings" and metrics[len(metrics) // 2] == 0:
                median = 1
            else:
                # 微妙
                median = (metrics[len(metrics) // 2] + 1) / 1
        else:
            median = metrics[len(metrics) // 2] / min_stress
        diff_x.append(round((optimal_cell_size - float(n)) * 100) / 100)
        y.append(median)

    obj = {"x": diff_x, "y": y}
    return obj


def main():
    with open("./graphSet0920/info_weigthed.json") as f:
        _graph_info = [g for g in json.load(f).values()]

    graph_info = list2dict(_graph_info)

    cell_size_files = []
    _dir = glob.glob("./journal/data/weigthing_liner/*")
    for d in _dir:
        files = glob.glob(d + "/log/*")
        cell_size_files.append(files)

    cell_size_files = sum(cell_size_files, [])
    print(len(cell_size_files))

    plt_x = {"stress": [], "CAM": [], "EC": [], "IEL": [], "NR": []}
    plt_y = {"stress": [], "CAM": [], "EC": [], "IEL": [], "NR": []}

    for filepath in cell_size_files:
        if os.path.isdir(filepath):
            continue
        with open(filepath) as f:
            data = json.load(f)
        file_name = re.split("[/]", filepath)[-1][:-6]
        print(file_name)

        # typeAは省く
        # if file_name in graph_info and (graph_info[file_name]["type"] == "a"):
        #     continue

        obj = get_metrics_raito(data, "stress")
        plt_x["stress"].append(obj["x"])
        plt_y["stress"].append(obj["y"])

        obj = get_metrics_raito(data, "edge_crossings")
        plt_x["EC"].append(obj["x"])
        plt_y["EC"].append(obj["y"])

        obj = get_metrics_raito(data, "ideal_edge_lengths")
        plt_x["IEL"].append(obj["x"])
        plt_y["IEL"].append(obj["y"])

        obj = get_metrics_raito(data, "crossing_angle_maximization")
        plt_x["CAM"].append(obj["x"])
        plt_y["CAM"].append(obj["y"])

        obj = get_metrics_raito(data, "node_resolution")
        plt_x["NR"].append(obj["x"])
        plt_y["NR"].append(obj["y"])

    len(plt_x["NR"])

    for metrics in plt_x.keys():
        # 散布図描画
        # sns.scatterplot(
        #     x=reduce(lambda a, b: a + b, plt_x), y=reduce(lambda a, b: a + b, plt_y))
        sns.boxplot(
            x=reduce(lambda a, b: a + b, plt_x[metrics]),
            y=reduce(lambda a, b: a + b, plt_y[metrics]),
            color="white",
            showfliers=False,
        )
        plt.title(metrics)

        # plt.ylim(bottom=1.0)
        plt.axhline(y=1.1, color="blue", ls="--")
        # plt.axhline(y=1.2, color="red", ls="--")

        plt.show()

        # print(reduce(lambda a, b: a + b, plt_x))


if __name__ == "__main__":
    main()
