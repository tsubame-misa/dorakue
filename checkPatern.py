"""
線形探索した最適値と黄金探索で求めた値がどの程度離れているか（平均ver）
"""

import glob
from networkx.readwrite import json_graph
import re
import json
import matplotlib.pyplot as plt
import glob
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

liner = "test_stress_liner_avarage_20_20loop"
golden = "honban_networkx_1014_20loop"

goldens = ["honban_networkx_1014_20loop", "honban_networkx_1014", "test_0102_honban_3_20_20loop", "test_0102_honban_3_20_20loop_2", "test_0102_honban_3_10_20loop"]

files = glob.glob("./graph_networkx_only/*")

graphs = []
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
    "qh882":"a", #際どい
    "dwt_1005":"a"
}
# dwt_1005 size 1005
# 1138_bus size 1138
# dwt_2680 size 2680
# 3elt size 4720

for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    file_name = re.split('[/.]', filepath)[3]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)

sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
result = []
scatter_x = []

data = []

for g in sorted_graphs:
    print(g["name"], "size", len(g["graph"].nodes))
    liner_log_file = glob.glob(liner+"/log/save_best_len_log/"+g["name"]+'-.json')
    with open(liner_log_file[0]) as f:
        liner_log = json.load(f)

    g_sum = []
    for gg in goldens:
        golden_log_file = glob.glob(gg+"/log/"+g["name"]+'-best*')   
        with open(golden_log_file[0]) as f:
            golden_log = json.load(f)
        g_sum.append(liner_log["best_multiple_num"] - golden_log["multiple_num"])
        # print(g["name"], liner_log["best_multiple_num"] - golden_log["multiple_num"], liner_log["best_multiple_num"] , golden_log["multiple_num"])
        # scatter_x.append(liner_log["best_multiple_num"] - golden_log["multiple_num"])
        # scatter_x.append(liner_log["best_multiple_num"])
        # print(g["name"], liner_log["best_multiple_num"])
    print(g_sum)

    data.append({"value":sum(g_sum)/len(g_sum),"type":graph_type[g["name"]]})


plt.figure(figsize=(6, 2)) 

# Swarm plot
# sns.swarmplot(x=scatter_x, color='#1581ed', alpha=0.5)

# 箱ひげ図
# sns.boxplot(x=scatter_x, color='white', width=0.2)

# plt.xlabel("Difference in optimal cell size between golden section search and linear search")



# print(scatter_x)
# print(data)


# # グラフの表示
# plt.show()


# DataFrameに変換

df = pd.DataFrame(data)

# Swarm plot
plt.figure(figsize=(10, 6))  # 図のサイズを調整
order = ['a', 'b', 'c', 'd']
sns.swarmplot(x='value', y='type', data=df, palette=sns.color_palette('Set2', n_colors=len(df['type'].unique())), order=order)
plt.xlabel("Difference between optimal values")

# グラフの表示
plt.show()

