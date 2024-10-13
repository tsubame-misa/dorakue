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


def list2dict(data):
    data_dict = {}
    for d in data:
        data_dict.update(d)
    return data_dict


def get_time_avg(data):
    times = [d["time"] for d in data]
    return sum(times) / len(times)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--small", default=106)  # 106
    parser.add_argument("--medium", default=500)  # 500
    args = parser.parse_args()
    small_point = int(args.small)
    medium_point = int(args.medium)

    files = {
        "./graphSet0920/networkx/*",
        "./graphSet0920/doughNetGraph/default/*",
        "./graphSet0920/doughNetGraph0920/*",
        "./graphSet0920/randomPartitionNetwork/*",
        "./graphSet0920/randomPartitionNetwork0920/*",
        "./graphSet0920/suiteSparse/*",
        "./graphSet0920/suiteSparse0920/*",
    }

    gss_file = {"./journal/data/weighting_gss/*"}

    with open("./graphSet0920/info_weigthed.json") as f:
        _graph_info = [g for g in json.load(f).values()]
    graph_info = list2dict(_graph_info)

    graph_dict = {}

    for f in files:
        files = glob.glob(f)
        for f in files:
            file_name = re.split("[/]", f)[-1][:-5]
            if not file_name in graph_info:
                continue

            graph = json_graph.node_link_graph(json.load(open(f)))
            graph_dict[file_name] = graph

    result = {"small": [], "medium": [], "large": []}
    result_liner = {"small": [], "medium": [], "large": []}
    compare_data = {}

    for gf in gss_file:
        dirs = glob.glob(gf)
        for d in dirs:
            files = glob.glob(d + "/log/*")
            for f in files:
                with open(f) as _f:
                    data = json.load(_f)
                time = get_time_avg(data)
                file_name = re.split("[/]", f)[-1][:-10]
                if not file_name in graph_info:
                    continue
                graph = graph_dict[file_name]
                compare_data[file_name] = {"gss": time}
                compare_data[file_name]["graph"] = graph

                if len(graph.nodes) <= small_point:
                    result["small"].append([time, len(graph.nodes), len(graph.edges)])
                elif len(graph.nodes) <= medium_point:
                    result["medium"].append([time, len(graph.nodes), len(graph.edges)])
                else:
                    result["large"].append([time, len(graph.nodes), len(graph.edges)])

    # print(compare_data)

    for lf in glob.glob("./journal/data/liner_all/log/*"):
        file_name = re.split("[/]", lf)[-1][:-10]

        with open(f) as _f:
            data = json.load(_f)
        time = get_time_avg(data) * 40
        file_name = re.split("[/]", lf)[-1][:-10]
        if not file_name in compare_data:
            continue
        compare_data[file_name]["liner"] = time
        compare_data[file_name]["rate"] = (
            compare_data[file_name]["gss"] / compare_data[file_name]["liner"]
        )
        print(
            file_name,
            compare_data[file_name]["gss"],
            compare_data[file_name]["liner"],
            compare_data[file_name]["rate"],
        )

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

    # Creating the scatter plot
    plt.scatter(nodes, time_rate)

    # Adding labels and title
    plt.xlabel("node values")
    plt.ylabel("time values")
    plt.title("Scatter Plot of Provided Data")

    # Display the plot
    plt.show()


if __name__ == "__main__":
    main()
