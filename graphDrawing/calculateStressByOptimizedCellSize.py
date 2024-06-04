
import glob
from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt
import csv
import matplotlib.pyplot as plt
import seaborn as sns

"""
ストレスがどの程度改善されたかを調べる
"""

def compare_graph(data, file_name, type,  cell_size, no_torus_stress, min_stress):
    print("---------------------------")
    print(file_name, type, cell_size)

    cnt = 0
    sub_cnt = 0
    for i, d in enumerate(data):
        if d["stress"]/min_stress <= 1.1 :
            # print(abs(d["multipl_number"] - cell_size), d["multipl_number"], cell_size)
            cnt += 1
        if d["stress"] < no_torus_stress:
            sub_cnt += 1
    
    csv_data = []
    
    pre_cell_size =  sorted([x["multipl_number"] for x in data])
    cell_size_diff = sorted([abs(cell_size - x["multipl_number"]) for x in data])
    print("cell size ave", sum(pre_cell_size)/len(data), sum(cell_size_diff)/len(cell_size_diff), 
            "mid", pre_cell_size[len(data)//2], cell_size_diff[len(data)//2])
    # csv_data.append(file_name,  sum(pre_cell_size)/len(data), abs(cell_size - sum(pre_cell_size)/len(data)),  pre_cell_size[len(data)//2], abs(cell_size - pre_cell_size[len(data)//2]))
    print("【ストレスが最小値の90~110%】", cnt, cnt/len(data))
    print("【非トーラスでの描画よりストレスが小さい】",sub_cnt, sub_cnt/len(data))

    # if  file_name=="octahedral" or file_name=="frucht" or file_name=="moebius_kantor" or file_name=="chvatal":
    #     # 散布図描画
    #     sns.scatterplot(x=[d["multipl_number"]-cell_size for i,d in enumerate(data)], y=[d["stress"] for i,d in enumerate(data)])
    #     plt.title(file_name)
    #     plt.axvspan(-0.1, 0.1, color="gray", alpha=0.3)
    #     if file_name=="octahedral":
    #         # 1.61 - 1.38 = 0.23
    #         plt.axvspan(-0.33, -0.13, color="blue", alpha=0.3)
    #     plt.show()
        



def main():
    files = glob.glob("./graphSet/networkx/*")

    cell_size_info = {}
    cell_size_files = glob.glob("./graphDrawing/data/my_algorithm/liner_networkx_0508_mid_20/log/save_best_len_log/*")
    # cell_size_files = glob.glob("./test_liner_0416_mid/log/save_best_len_log/*")
    # cell_size_files = glob.glob("./ pacificvis2024_log/networkX/test_stress_liner_avarage_20_20loop/log/save_best_len_log/*")

    for filepath in cell_size_files:
        with open(filepath) as f:
            data = json.load(f)
        file_name = re.split('[/.-]', filepath)[8]
        # file_name = re.split('[/.-]', filepath)[7]
        cell_size_info[file_name] = {"cellSize":data["best_multiple_num"], "noTorusStress":data["y"][-1], "minStress":data["best_stress_comp"]}

    with open("./graphSet/info202405.json") as f:
        graph_info = json.load(f)

    # 使用するグラフをノード数順に並び替える
    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/.]', filepath)[4]
        # typeA, Dは省く
        # if graph_info["Networkx"][file_name]["type"] == "a" or graph_info["Networkx"][file_name]["type"] == "d":
        #     continue
        obj = {"name": file_name, "graph": graph, "type":graph_info["Networkx"][file_name]["type"]}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

    # print(cell_size_info)

    for g in sorted_graphs:
        # if g["name"] != "chvatal":
        #     continue
        # log_file_candidate = glob.glob("./test_dought_0509_20_not_new/"+"/log/"+g["name"]+'-all*')
        log_file_candidate = glob.glob("./graphDrawing/data/my_algorithm/networkx_0508_20/"+"/log/"+g["name"]+'-all*')
        if len(log_file_candidate)==0:
            continue
        with open(log_file_candidate[0]) as f:
            log_file = json.load(f)
            compare_graph(log_file, g["name"], g["type"], cell_size_info[g["name"]]["cellSize"], cell_size_info[g["name"]]["noTorusStress"],  cell_size_info[g["name"]]["minStress"])
    
    

if __name__ == '__main__':
    main()