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
20回の描画での評価指標がどの程度バラけているのかの確認
"""


def get_data_diff(data):
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
    avg = {
        "stress": sum(stress) / n,
        "edge_crossings": sum(ec) / n,
        "edge_length_vaiance": sum(elv) / n,
        "minimum_angle": sum(ma) / n,
        "node_resolution": sum(nr) / n,
    }

    diff_data = []
    for d in data:
        obj = {
            "stress": d["stress"] - avg["stress"],
            "edge_crossings": d["edge_crossings"] - avg["edge_crossings"],
            "edge_length_vaiance": d["edge_length_vaiance"]
            - avg["edge_length_vaiance"],
            "minimum_angle": d["minimum_angle"] - avg["minimum_angle"],
            "node_resolution": d["node_resolution"] - avg["node_resolution"],
        }
        diff_data.append(obj)
    return diff_data


def show_box_plot(data, title):
    # データフレームの作成
    df = pd.DataFrame(data)

    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df.drop(columns=["node_resolution"]))
    plt.xticks(rotation=45)
    plt.title(title)
    plt.show()


def list2dict(data):
    data_dict = {}
    for d in data:
        data_dict.update(d)
    return data_dict


def main():
    chen_files = [
        "./journal/data/chen/chen_torus_cell_size_networkx/log/*",
        # "./journal/data/chen/chen_torus_cell_size_dough/log/*",
        # "./journal/data/chen/chen_torus_cell_size_random/log/*",
        # "./journal/data/chen/chen_torus_cell_size_sparse/log/*",
        # "./journal/data/chen/chen_networkx_50/log/*"
    ]
    optimal_files = [
        # "./journal/data/optimal/optimal_torus_cell_size_networkx/log/*",
        # "./journal/data/optimal/optimal_torus_cell_size_dough/log/*",
        # "./journal/data/optimal/optimal_torus_cell_size_random/log/*",
        # "./journal/data/optimal/optimal_torus_cell_size_sparse/log/*",
        "./journal/data/optimal/optimal_networkx_50/log/*"
    ]

    for files_name in optimal_files:
        files = glob.glob(files_name)
        for file in files:
            with open(file) as f:
                data = json.load(f)
            name = re.split("[/]", file)[-1][:-10]
            show_box_plot(get_data_diff(data), name)

    exit()

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
