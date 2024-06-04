
import glob
from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt
import csv
import matplotlib.pyplot as plt
import seaborn as sns

"""
セルサイズと真値の差が0.1以下かどうかを調べる
"""

def compare_graph(data, file_name, cell_size, max_stress):
    print("---------------------------")
    print(file_name, cell_size, max_stress)

    cnt = 0
    sub_cnt = 0
    less_cnt = 0
    for i, d in enumerate(data):
        # print(d["stress"], d["stress"]/max_stress, round(d["stress"]/max_stress, 1))
        # if file_name=="octahedral" and abs(d["multiple_num"] - 1.38) <= 0.1:
        #     cnt += 1
        if round(abs(d["multiple_num"] - cell_size),1) <= 0.1 :
            # print(abs(d["multiple_num"] - cell_size), d["multiple_num"], cell_size)
            cnt += 1
        elif d["stress"]/max_stress <= 0.75 :
            sub_cnt += 1
        
        if round(d["stress"]/max_stress, 1) <= 1 :
            less_cnt += 1
    
    csv_data = []
    
    pre_cell_size =  sorted([x["multiple_num"] for x in data])
    cell_size_diff = sorted([abs(cell_size - x["multiple_num"]) for x in data])
    print("cell size ave", sum(pre_cell_size)/len(data), sum(cell_size_diff)/len(cell_size_diff), 
            "mid", pre_cell_size[len(data)//2], cell_size_diff[len(data)//2])
    # csv_data.append(file_name,  sum(pre_cell_size)/len(data), abs(cell_size - sum(pre_cell_size)/len(data)),  pre_cell_size[len(data)//2], abs(cell_size - pre_cell_size[len(data)//2]))
    print("【セルサイズが 真値の+-0.1以内】", cnt, cnt/len(data))
    print("【上記以外で二次元平面での描画よりもストレスが0.75倍に改善された数】",sub_cnt, sub_cnt/len(data))
    print("【ストレスが非トーラスよりも良い数】", less_cnt, less_cnt/len(data))

    # if  file_name=="hoffman_singleton" or file_name=="tutte" or file_name=="moebius_kantor" or file_name=="sedgewick_maze" or file_name=="house_x":
    #     # 散布図描画
    #     sns.scatterplot(x=[d["multiple_num"]-cell_size for i,d in enumerate(data)], y=[d["stress"] for i,d in enumerate(data)])
    #     plt.title(file_name)
    #     plt.axvspan(-0.1, 0.1, color="gray", alpha=0.3)
    #     if file_name=="octahedral":
    #         # 1.61 - 1.38 = 0.23
    #         plt.axvspan(-0.33, -0.13, color="blue", alpha=0.3)
    #     # plt.axvline(x=0.1)
    #     # plt.axvline(x=-0.1)
    #     plt.show()
        



def main():
    files = glob.glob("./graphSet/networkx/*")

    cell_size_info = {}
    cell_size_files = glob.glob("./graphDrawing/data/egraph/liner_egraph_networkx_20/log/save_best_len_log/*")
    # cell_size_files = glob.glob("./test_liner_0416_mid/log/save_best_len_log/*")
    # cell_size_files = glob.glob("./ pacificvis2024_log/networkX/test_stress_liner_avarage_20_20loop/log/save_best_len_log/*")
    for filepath in cell_size_files:
        with open(filepath) as f:
            data = json.load(f)
        file_name = re.split('[/]', filepath)[-1][:-6]
        cell_size_info[file_name] = {"cellSize":data["best_multiple_num"], "maxStress":data["y"][-1]}

    with open("./graphSet/info202405_egraph.json") as f:
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

    # print(cell_size_info)

    for g in sorted_graphs:
        # if g["name"] != "chvatal":
        #     continue
        log_file_candidate = glob.glob("./graphDrawing/data/egraph/range_check/egraph_networkx_20_0-3.5/log/"+g["name"]+'-all*')
        log_file_candidate = glob.glob("./regenerate_test/log/"+g["name"]+'-all*')
        
        if len(log_file_candidate)==0:
            continue
        with open(log_file_candidate[0]) as f:
            log_file = json.load(f)
            compare_graph(log_file, g["name"], cell_size_info[g["name"]]["cellSize"], cell_size_info[g["name"]]["maxStress"])
    
    

if __name__ == '__main__':
    main()