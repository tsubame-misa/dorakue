
import glob
from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt
import csv
import matplotlib.pyplot as plt
import seaborn as sns

"""
美的評価指標の評価
"""

def compare_graph(data, file_name, type,  max_stress):
    print("---------------------------")
    print(file_name, type, max_stress)

    sub_cnt = 0
    less_cnt = 0
    for i, d in enumerate(data):
        if round(d["stress"]/max_stress, 2) <= 0.75 :
            sub_cnt += 1
        
        if round(d["stress"]/max_stress, 2) <= 1 :
            less_cnt += 1
    
    print("【ストレスが非トーラスよりも良い数】", less_cnt, less_cnt/len(data))
    print("【ストレスが非トーラスよりも75%以下の数】",sub_cnt, sub_cnt/len(data))
        

def getStressAvg(data):
    return sum([d["stress"] for d in data])/len(data)


def main():
    files = glob.glob("./graphSet/networkx/*")

    with open("./graphSet/info202405_egraph.json") as f:
        graph_info = json.load(f)

    # 使用するグラフをノード数順に並び替える
    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/.]', filepath)[4]
        base_file = glob.glob("./test_2d_sgd/log/"+file_name+"-all-.json")
        if len(base_file)==0:
            continue
        with open(base_file[0]) as f:
            data = json.load(f)
        stress_avg = getStressAvg(data)
        print(stress_avg)

        # typeA, Dは省く
        # if graph_info["Networkx"][file_name]["type"] == "a" or graph_info["Networkx"][file_name]["type"] == "d":
        #     continue
        obj = {"name": file_name, "graph": graph, "type":graph_info["Networkx"][file_name]["type"],  "stressAvg":stress_avg}
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
            compare_graph(log_file, g["name"], g["type"],  g["stressAvg"])
    
    

if __name__ == '__main__':
    main()