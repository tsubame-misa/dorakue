
import glob
from networkx.readwrite import json_graph
import json
from algorithm.SGDBase.torusGoldenSearchSGD import torus_golden_search
import re
import matplotlib.pyplot as plt
import seaborn as sns


def create_graph(data, file_name):
    # データの整形
    formatted_data = {
        "Data": [],
        "Multipl Number": [],
        "Stress": [],
    }

    for i, d in enumerate(data):
        # for key in ["avg1", "scaled", "pre"]:
        for key in ["scaled"]:
            formatted_data["Data"].append(key)
            formatted_data["Multipl Number"].append(d[key]["multipl_number"])
            formatted_data["Stress"].append(d[key]["stress"])
    

    print("---------------------------")
    print(file_name, "stress")

    # avg1_stress =  sorted([x["avg1"]["stress"] for x in data])
    # print("avg1 ave", sum(avg1_stress)/len(data), "mid", avg1_stress[len(data)//2])

    # pre_stress =  sorted([x["pre"]["stress"] for x in data])
    # print("pre ave", sum(pre_stress)/len(data), "mid", pre_stress[len(data)//2])

    scaled_stress=  sorted([x["scaled"]["stress"] for x in data])
    print("scaled ave", sum(scaled_stress)/len(data), "mid", scaled_stress[len(data)//2])
    print()

    # 散布図描画
    sns.scatterplot(data=formatted_data, x="Multipl Number", y="Stress", hue="Data", alpha=0.8)
    plt.title(file_name)
    plt.show()



def main():
    files = glob.glob("./graphSet/networkx/*")

    with open("./graphSet/info2.json") as f:
        graph_info = json.load(f)

    # 使用するグラフをノード数順に並び替える
    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/.]', filepath)[4]
        # typeA, Dは省く
        if graph_info["Networkx"][file_name]["type"] == "a" or graph_info["Networkx"][file_name]["type"] == "d":
            continue
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

    for g in sorted_graphs:
        log_file_candidate = glob.glob("./test/"+"/log/"+g["name"]+'-all*')
        if len(log_file_candidate)==0:
            continue
        with open(log_file_candidate[0]) as f:
            log_file = json.load(f)
            create_graph(log_file, g["name"])
    

if __name__ == '__main__':
    main()