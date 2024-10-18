import argparse
import glob
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + "/")

import glob
from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt


def get_time_avg(data):
    times = [d["time"] for d in data]
    return sum(times) / len(times)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("liner_data_dir")
    parser.add_argument("gss_data_dir")
    parser.add_argument("--small", default=106)  # 106
    parser.add_argument("--medium", default=500)  # 500

    args = parser.parse_args()
    liner_data_dir = args.liner_data_dir
    gss_data_dir = args.gss_data_dir
    small_point = int(args.small)
    medium_point = int(args.medium)

    graph_dict = {}
    for f in glob.glob("./graphSet0920/*"):
        files = glob.glob(f + "/*")
        for f in files:
            file_name = re.split("[/]", f)[-1][:-5]
            graph = json_graph.node_link_graph(json.load(open(f)))
            graph_dict[file_name] = graph

    result = {"small": [], "medium": [], "large": []}
    result_liner = {"small": [], "medium": [], "large": []}
    compare_data = {}

    for f in glob.glob(gss_data_dir + "/log/*"):
        with open(f) as _f:
            data = json.load(_f)
        time = get_time_avg(data)
        file_name = re.split("[/]", f)[-1][:-10]
        graph = graph_dict[file_name]
        compare_data[file_name] = {"gss": time}
        compare_data[file_name]["graph"] = graph

        if len(graph.nodes) <= small_point:
            result["small"].append([time, len(graph.nodes), len(graph.edges)])
        elif len(graph.nodes) <= medium_point:
            result["medium"].append([time, len(graph.nodes), len(graph.edges)])
        else:
            result["large"].append([time, len(graph.nodes), len(graph.edges)])

    print(len(compare_data.values()))

    for lf in glob.glob(liner_data_dir + "/log/*"):
        file_name = re.split("[/]", lf)[-1][:-10]

        with open(f) as _f:
            data = json.load(_f)
        # 線形で0-4の範囲を探す場合は 0.1刻み(許容範囲刻み) で 40回の繰り返しのため 40をかけて概算
        time = get_time_avg(data) * 40
        file_name = re.split("[/]", lf)[-1][:-10]
        if not file_name in compare_data:
            continue
        compare_data[file_name]["liner"] = time
        compare_data[file_name]["rate"] = (
            compare_data[file_name]["gss"] / compare_data[file_name]["liner"]
        )
        # print(
        #     file_name,
        #     compare_data[file_name]["gss"],
        #     compare_data[file_name]["liner"],
        #     compare_data[file_name]["rate"],
        # )
        graph = graph_dict[file_name]
        if len(graph.nodes) <= small_point:
            result_liner["small"].append([time, len(graph.nodes), len(graph.edges)])
        elif len(graph.nodes) <= medium_point:
            result_liner["medium"].append([time, len(graph.nodes), len(graph.edges)])
        else:
            result_liner["large"].append([time, len(graph.nodes), len(graph.edges)])

    print("gss-----------------")
    for key in result:
        print(
            key,
            sum(result[key][0]) / len(result[key]),
            len(result[key]),
        )

    print("liner-----------------")
    for key in result_liner:
        print(
            key,
            sum(result_liner[key][0]) / len(result_liner[key]),
            len(result_liner[key]),
        )

    time_rate = [item["rate"] for item in compare_data.values()]
    nodes = [len(item["graph"].nodes) for item in compare_data.values()]

    plt.scatter(nodes, time_rate)
    plt.xlabel("node values")
    plt.ylabel("time values")
    plt.axhline(y=1.0, color="blue", ls="--")
    # 計算上ではgssは線形で実行した場合の18%の時間で実行できるはず
    plt.axhline(y=0.2, color="red", ls="--")
    plt.show()


if __name__ == "__main__":
    main()
