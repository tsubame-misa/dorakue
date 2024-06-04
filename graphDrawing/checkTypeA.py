
import glob
from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt
import csv
import matplotlib.pyplot as plt
import seaborn as sns

"""
タイプAのグラフに対して、セルサイズと回り込みの数から描画結果が非トーラスになっているかを調べる
"""


def compare_graph(data, file_name, cell_size, max_stress, stop_size, type):
    print("---------------------------")
    print(file_name, type, cell_size, stop_size)

    if stop_size is None:
        stop_size = 4

    cnt = 0
    sub_cnt = 0
    stress_cnt = 0
    for i, d in enumerate(data):
        # print(d["stress"])
        # if file_name=="octahedral" and abs(d["multiple_num"] - 1.38) <= 0.1:
        #     cnt += 1
        print(d["edge_crossings"])
        if min(cell_size, stop_size) <= d["multiple_num"]:
            cnt += 1
        ## 画面の中心を整える必要がある
        if d["edge_crossings"] == 0:
            sub_cnt += 1
        elif d["stress"]/max_stress <= 1.1:
            stress_cnt += 1
    
    csv_data = []
    
    pre_cell_size =  sorted([x["multiple_num"] for x in data])
    print("cell size ave", sum(pre_cell_size)/len(data), "mid", pre_cell_size[len(data)//2], )
    # csv_data.append(file_name,  sum(pre_cell_size)/len(data), abs(cell_size - sum(pre_cell_size)/len(data)),  pre_cell_size[len(data)//2], abs(cell_size - pre_cell_size[len(data)//2]))
    print("【セルサイズが基点よりも大きいもの】", cnt, cnt/20)
    print("【エッジの回り込みがないもの】",sub_cnt, sub_cnt/20)
    print("【エッジの回り込みがあるがストレスが1.1倍以下に収まっているもの】", stress_cnt)

    if  file_name=="octahedral" or file_name=="heawood" or file_name=="moebius_kantor" or file_name=="sedgewick_maze":
        # 散布図描画
        sns.scatterplot(x=[d["multiple_num"]-cell_size for i,d in enumerate(data)], y=[d["stress"] for i,d in enumerate(data)])
        plt.title(file_name)
        plt.axvspan(-0.1, 0.1, color="gray", alpha=0.3)
        if file_name=="octahedral":
            # 1.61 - 1.38 = 0.23
            plt.axvspan(-0.33, -0.13, color="blue", alpha=0.3)
        # plt.axvline(x=0.1)
        # plt.axvline(x=-0.1)
        plt.show()
        

def findStopCellSize(data):
    for i in range(len(data["y"])-5):
        find = True
        for j in range(5):
            if abs(data["y"][i] - data["y"][i+j]) > data["y"][i]*0.025:
                find = False
                break
        if find:
            return data["x"][i]


def main():
    files = glob.glob("./graphSet/networkx/*")

    cell_size_info = {}
    cell_size_files = glob.glob("./graphDrawing/data/egraph/liner_egraph_networkx_20/log/save_best_len_log/*")
    
    for filepath in cell_size_files:
        with open(filepath) as f:
            data = json.load(f)
        file_name = re.split('[/]', filepath)[-1][:-6]
        cell_size_info[file_name] = {"cellSize":data["best_multiple_num"], "maxStress":data["y"][-1], "stopCellSize":findStopCellSize(data)}

    with open("./graphSet/info202405_egraph.json") as f:
        graph_info = json.load(f)

    for c in cell_size_info:
        print(c, graph_info["Networkx"][c]["type"], cell_size_info[c])

    # 使用するグラフをノード数順に並び替える
    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/]', filepath)[-1][:-5]
        if not(graph_info["Networkx"][file_name]["type"] == "a" or graph_info["Networkx"][file_name]["type"] == "d"):
            continue
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

    for g in sorted_graphs:
        log_file_candidate = glob.glob("./graphDrawing/data/egraph/range_check/egraph_networkx_20_0-3.5"+"/log/"+g["name"]+'-all*')
        if len(log_file_candidate)==0:
            continue
        with open(log_file_candidate[0]) as f:
            log_file = json.load(f)
            compare_graph(log_file, g["name"], cell_size_info[g["name"]]["cellSize"], cell_size_info[g["name"]]["maxStress"],cell_size_info[g["name"]]["stopCellSize"], graph_info["Networkx"][file_name]["type"])
    
    

if __name__ == '__main__':
    main()