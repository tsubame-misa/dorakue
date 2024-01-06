import glob
from networkx.readwrite import json_graph
import re
import json
import csv
from common import initGraph
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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



torus_files = "honban_random_1014"
sgd_files = "honban_random_1014_chen"
    
# # chen2021
# torus_files = "honban_chen2021_1014_20loop"
# sgd_files = "honban_chen2021_1014_chen_20loop"

torus_files = "honban_chen2020_1014_20loop"
sgd_files = "honban_chen202_1014_chen_20loop"

#networkx
# torus_files = "honban_networkx_1014_20loop"
# sgd_files = "honban_networkx_1014_chen_20loop"


# files = glob.glob("./graph_networkx_only/*")
# files = glob.glob("./scallFreeGraph2/*")
# files = glob.glob("./randomGraphs/*")
files = glob.glob("./doughNetGraph/default/*")
# files = glob.glob("./chen2021Graph/*")

graphs = []

for filepath in files:
    if filepath[-3:]=="txt":
        continue
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    file_name = re.split('[/.]', filepath)[4]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)

sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
result = [["name","node", "type", "stress", "edge crossing", "edge length variance", "incidence angle", "node resolution"]]
comp_result = [["name","node", "stress", "edge crossing", "edge length variance", "incidence angle", "node resolution"]]
order = ["stress", "edge_crossings", "edge_length_variance", "minimum_angle", "node_resolution"]
box_data = {"edge_length_variance":[],"minimum_angle":[], "edge_crossings":[], "stress":[], "node_resolution":[]}


for g in sorted_graphs:
    print(g["name"], "size", len(g["graph"].nodes))

    torus_log_file = glob.glob(torus_files+"/log/"+g["name"]+'-best*')
    sgd_log_file = glob.glob(sgd_files+"/log/"+g["name"]+'-best*')

    print(torus_log_file)
    print(sgd_log_file)

    with open(torus_log_file[0]) as f:
        torus_log = json.load(f)
    with open(sgd_log_file[0]) as f:
        sgd_log = json.load(f)

    maxd = initGraph.get_maxd(graph, file_name)
    
    torus_row = [g["name"], len(g["graph"].nodes), "our", torus_log["stress"],torus_log["edge_crossings"],
                torus_log["edge_length_variance"], torus_log["minimum_angle"], torus_log["node_resolution"], torus_log["multiple_num"]]
    sgd_row = [g["name"], len(g["graph"].nodes), "chen",  sgd_log["stress"], sgd_log["edge_crossings"], 
                sgd_log["edge_length_variance"], sgd_log["minimum_angle"], sgd_log["node_resolution"], "", ""]
    result.append(torus_row)
    result.append(sgd_row)
    
    torus_row = [g["name"], len(g["graph"].nodes),  sgd_log["stress"]/torus_log["stress"],  sgd_log["edge_crossings"]/torus_log["edge_crossings"] if torus_log["edge_crossings"]!=0 else 1,
                sgd_log["edge_length_variance"]/torus_log["edge_length_variance"], sgd_log["minimum_angle"]/torus_log["minimum_angle"], sgd_log["node_resolution"]/torus_log["node_resolution"]]
    comp_result.append(torus_row)

    for k in order:
        if k=="edge_crossings":
            v =sgd_log["edge_crossings"]/torus_log["edge_crossings"] if torus_log["edge_crossings"]!=0 else 1
            if v==0:
                v = 1
        else:
            v =  sgd_log[k]/torus_log[k]
        box_data[k].append(v)

avarage = ["-", "-", "avarage"]
for k in order:
    df = pd.DataFrame(box_data[k])
    print(box_data[k])

    avg = sum([v for v in box_data[k]])/len(box_data[k])
    avarage.append(avg)

    # Swarm plot
    plt.figure(figsize=(10, 6))  # 図のサイズを調整
    # sns.boxplot(y=box_data[k], color='white', order=order, width=0.2, sym="")
    sns.boxplot(y=box_data[k], color='white', order=order, width=0.2)

    plt.ylabel(k)

    plt.axhline(y=1, color='blue', linestyle='--', label='value=1')
    plt.legend()
 
    # グラフの表示
    plt.show() 



result.append(avarage)
comp_result.append(avarage)

create_csv_data(result, "all")
create_csv_data(comp_result, "only")