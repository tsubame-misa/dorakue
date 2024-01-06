import glob
from networkx.readwrite import json_graph
import re
import json
import csv
from common import initGraph
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


graph_type = {
    "diamond":"d",
    "house":"b",
    "bull":"a", 
    "house_x":"d", 
    "octahedral":"b",
    "cubical":"c",
    "sedgewick_maze":"c", #際どい
    "petersen":"b", 
    "krackhardt_kite":"a", 
    "frucht":"b",
    "chvatal":"c", 
    "icosahedral":"c", 
    "heawood":"b", 
    "florentine_families": "a",
    "moebius_kantor":"b", 
    "pappus":"b",
    "desargues":"c", 
    "dodecahedral":"c" ,
    "davis_southern_women":"a", 
    "karate_club":"a", 
    "tutte":"b",
    "hoffman_singleton":"b",
    "les_miserables":"a", 
}
    # "qh882":"a", #際どい
    # "dwt_1005":"a",
    # "1138_bus":"a"
# dwt_2680 size 2680
# 3elt size 4720

def create_csv_data(csv_data):
    head = ["name", "node", "type", "edge_length_variance",
            "minimum_angle", "edge_crossings", "stress", "comp_stress", "multiple_num"]
    
    # CSVファイル名
    csv_file = "compare_result.csv"

    # CSVファイルにデータを書き込む
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # ヘッダー行を書き込む
        writer.writerow(head)

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



# torus_files = "test_1227_honban_3_25_20loop"
# sgd_files = "test_1227_sgd_honban"

torus_files = "honban_networkx_1014_20loop"
sgd_files = "honban_networkx_1014_chen_20loop"

# torus_files = "random_graph_test"
# sgd_files = "random_graph_test_chen"

# files = glob.glob("./graph/*")
# files = glob.glob("./scallFreeGraph2/*")
# files = glob.glob("./chen2021Graph/*")
files = glob.glob("./graph_networkx_only/*")
graphs = []

for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    file_name = re.split('[/.]', filepath)[3]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)

sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
result = []
scatter_x = []
scatter_y = []

data_per_type_torus = {"a":[], "b":[], "c":[], "d":[]}
data_per_type = {"a":[], "b":[], "c":[], "d":[]}

box_data = {"edge_length_variance":[],"minimum_angle":[], "edge_crossings":[], "stress":[]}

for g in sorted_graphs:
    print(g["name"], "size", len(g["graph"].nodes))
    if len(g["graph"].nodes) > 455:
        continue


    torus_log_file = glob.glob(torus_files+"/log/"+g["name"]+'-best*')
    sgd_log_file = glob.glob(sgd_files+"/log/"+g["name"]+'-best*')

    print(torus_log_file)
    print(sgd_log_file)

    with open(torus_log_file[0]) as f:
        torus_log = json.load(f)
    with open(sgd_log_file[0]) as f:
        sgd_log = json.load(f)

    maxd = initGraph.get_maxd(graph, file_name)

    print(torus_log["edge_crossings"], type(torus_log["edge_crossings"]))
    print( sgd_log["edge_crossings"]/(torus_log["edge_crossings"] if torus_log["edge_crossings"]!=0 else 1))

    torus_row = [g["name"], len(g["graph"].nodes), "torus", 
                sgd_log["edge_length_variance"]/torus_log["edge_length_variance"], sgd_log["minimum_angle"]/torus_log["minimum_angle"], torus_log["edge_crossings"],
                  torus_log["stress"], sgd_log["stress"]/torus_log["stress"],  sgd_log["edge_crossings"]/(torus_log["edge_crossings"] if torus_log["edge_crossings"]!=0 else 1)]
    sgd_row = [g["name"], len(g["graph"].nodes), "sgd", 
                sgd_log["edge_length_variance"], sgd_log["minimum_angle"], sgd_log["edge_crossings"], sgd_log["stress"] , "", ""]
    
    result.append(torus_row)

    scatter_x.append(torus_log["multiple_num"])
    scatter_y.append(sgd_log["stress"]/torus_log["stress"])

    data_per_type[graph_type[g["name"]]].append(sgd_row)
    data_per_type_torus[graph_type[g["name"]]].append(torus_row)

    for k in box_data:
        if k=="edge_crossings":
            v =sgd_log["edge_crossings"]/(torus_log["edge_crossings"] if torus_log["edge_crossings"]!=0 else 1)
            if v==0:
                v = 1
        else:
            v =  sgd_log[k]/torus_log[k]
        box_data[k].append({"value": v, "type":graph_type[g["name"]]})

type_result = []

for t in ["a", "b", "c", "d"]:
    edge_length_variance = sum([v[3] for v in data_per_type_torus[t]])/len(data_per_type_torus[t])
    minimum_angle = sum([v[4] for v in data_per_type_torus[t]])/len(data_per_type_torus[t])
    edge_crossings = sum([v[8] for v in data_per_type_torus[t]])/len(data_per_type_torus[t])
    stress_raito =  sum([v[7] for v in data_per_type_torus[t]])/len(data_per_type_torus[t])
    #  stress & edge crossing & edge length variance & incidence angle
    torus_row = [t, "torus", stress_raito, edge_crossings, edge_length_variance, minimum_angle]

    # edge_length_variance = sum([v[3] for v in data_per_type[t]])/len(data_per_type[t])
    # minimum_angle = sum([v[4] for v in data_per_type[t]])/len(data_per_type[t])
    # edge_crossings = sum([v[5] for v in data_per_type[t]])/len(data_per_type[t])
    # sgd_row = [t, "torus", edge_length_variance, minimum_angle, edge_crossings, stress_raito]


    type_result.append(torus_row)
    # result.append(sgd_row)
    
create_csv_data(type_result)

# # crate_scatter_plt(scatter_x, scatter_y)

for key in ["edge_length_variance","minimum_angle", "edge_crossings", "stress"]:

    df = pd.DataFrame(box_data[key])


    # Swarm plot
    plt.figure(figsize=(10, 6))  # 図のサイズを調整
    order = ['a', 'b', 'c', 'd']
    #sns.boxplot(x='type', y='value', data=df, palette=sns.color_palette('Set2', n_colors=len(df['type'].unique())), order=order)
    sns.boxplot(x='type', y='value', data=df, color='white', order=order, width=0.5, sym="")
    plt.ylabel(key)
    
    plt.axhline(y=1, color='blue', linestyle='--', label='value=1')
    plt.legend()

    # グラフの表示
    plt.show()