"""
jsonのposから評価し直す。なお互換性がすこぶるない
"""
import glob
from networkx.readwrite import json_graph
import re
import json
import csv
from common import initGraph, aestheticsMeasures
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import networkx as nx

def create_csv_data(csv_data, file_name="result"):
    # CSVファイル名
    csv_file = file_name + ".csv"

    # CSVファイルにデータを書き込む
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # データ行を書き込む
        writer.writerows(csv_data)


def crate_scatter_plt(x, y):
    plt.axhline(y=1, color='r', linestyle='--')
    plt.scatter(x, y, label='torus_maxd_y')

    plt.xlabel('times')
    plt.ylabel('compare stress')
    plt.title('')
    plt.legend()

    plt.show()


torus_files = "test_0102_honban_3_20_20loop_2"
sgd_files = "test_0102_honban_chen_max"

files = glob.glob("./graph/*")
graphs = []

for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    file_name = re.split('[/.]', filepath)[3]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)

result = [["name","node", "stress", "edge crossing", "edge length variance", "incidence angle"]]
comp_result = [["name","node", "stress", "edge crossing", "edge length variance", "incidence angle"]]
order = ["stress", "edge_crossings", "edge_length_variance", "minimum_angle"]
box_data = {"edge_length_variance":[],"minimum_angle":[], "edge_crossings":[], "stress":[]}


sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
for g in sorted_graphs:
    print(g["name"], "size", len(g["graph"].nodes))
    if len(g["graph"].nodes) > 1200:
        continue

    torus_log_file = glob.glob(torus_files+"/log/"+g["name"]+'-best*')
    sgd_log_file = glob.glob(sgd_files+"/log/"+g["name"]+'-best*')

    print(torus_log_file)
    print(sgd_log_file)

    with open(torus_log_file[0]) as f:
        torus_log = json.load(f)
    with open(sgd_log_file[0]) as f:
        sgd_log = json.load(f)

    diameter = nx.diameter(g["graph"])

    size = diameter * torus_log["multiple_num"]
    maxd = initGraph.get_maxd(g["graph"], file_name, True, 1/size)
    d = initGraph.get_shortest_path(g["graph"], file_name, True, 1/size)
    torus_pos = dict()
    for p in torus_log["pos"]:
        if p[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            torus_pos[int(p)] = torus_log["pos"][p]
        else:
            torus_pos[p] = torus_log["pos"][p]
    new_torus_log = aestheticsMeasures.calc_egraph_torus_evaluation_values(g["graph"], torus_pos, maxd, d, 1/size)
    new_torus_log["multiple_num"] = torus_log["multiple_num"]

    size = diameter * sgd_log["multiple_num"]
    maxd = initGraph.get_maxd(g["graph"], file_name, True, 1/size)
    d = initGraph.get_shortest_path(g["graph"], file_name, True, 1/size)
    chen_pos = dict()
    for p in sgd_log["pos"]:
        if p[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            chen_pos[int(p)] = sgd_log["pos"][p]
        else:
            chen_pos[p] = sgd_log["pos"][p]
    new_chen_log = aestheticsMeasures.calc_egraph_torus_evaluation_values(g["graph"], chen_pos, maxd, d, 1/size)
    new_chen_log["multiple_num"] = sgd_log["multiple_num"]

    torus_row = [g["name"], len(g["graph"].nodes), "torus", new_torus_log["stress"],new_torus_log["edge_crossings"],
                new_torus_log["edge_length_variance"], new_torus_log["minimum_angle"], new_torus_log["multiple_num"]]
    sgd_row = [g["name"], len(g["graph"].nodes), "sgd",  new_chen_log["stress"], new_chen_log["edge_crossings"], 
                new_chen_log["edge_length_variance"], new_chen_log["minimum_angle"], new_chen_log["multiple_num"]]
    result.append(torus_row)
    result.append(sgd_row)
    
    torus_row = [g["name"], len(g["graph"].nodes), "compare",  new_chen_log["stress"]/new_torus_log["stress"],  new_chen_log["edge_crossings"]/new_torus_log["edge_crossings"] if new_torus_log["edge_crossings"]!=0 else 1,
                new_chen_log["edge_length_variance"]/new_torus_log["edge_length_variance"], new_chen_log["minimum_angle"]/new_torus_log["minimum_angle"]]
    comp_result.append(torus_row)

    for k in order:
        if k=="edge_crossings":
            v =new_chen_log["edge_crossings"]/new_torus_log["edge_crossings"] if new_torus_log["edge_crossings"]!=0 else 1
            if v==0:
                v = 1
        else:
            v =  new_chen_log[k]/new_torus_log[k]
        box_data[k].append(v)

avarage = ["-", "-", "avarage"]

for k in order:
    df = pd.DataFrame(box_data[k])
    print(box_data[k])
    print()


    # Swarm plot
    plt.figure(figsize=(10, 6))  # 図のサイズを調整
    # sns.boxplot(y=box_data[k], color='white', order=order, width=0.2, sym="")
    sns.boxplot(y=box_data[k], color='white', order=order, width=0.2)


    avg = sum([v for v in box_data[k]])/len(box_data[k])
    avarage.append(avg)

    plt.ylabel(k)

    plt.axhline(y=1, color='blue', linestyle='--', label='value=1')
    plt.legend()
 
    # グラフの表示
    plt.show() 

result.append(avarage)
comp_result.append(avarage)

create_csv_data(result, "all")
create_csv_data(comp_result, "only")