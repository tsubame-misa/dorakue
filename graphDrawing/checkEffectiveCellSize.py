"""
ストレス許容誤差を調べる
+-1.5 でストレスが最小値の何倍になるかをboxplotで表示
+-0.75くらいで切りたい気持ちがあるが...
"""


import glob
import json
import math
import os
import re
from functools import reduce
import matplotlib.pyplot as plt
import seaborn as sns


    
def get_stress(data, filename):
    min_stress = data["best_stress_comp"]
    optimal_cell_size = data["best_multiple_num"]

    x = []
    y = []
    
    safe_diff = []
    for i in range(len(data["x"])):
        # print(data["x"][i], data["y"][i],  min_stress, abs(data["y"][i] - min_stress) )
        if abs(data["x"][i] - optimal_cell_size) <= 0.15:
            y.append(math.floor(data["y"][i]/min_stress*100)/100)
            x.append(round((data["x"][i]-optimal_cell_size)*100)/100)
    
    # print(filename, optimal_cell_size, min_stress, safe_diff)
    print(filename,optimal_cell_size, x)
    obj = {"x":x, "y":y}
    return obj


def main():
    with open("./graphSet/info202405.json") as f:
        graph_info = json.load(f)
   
    cell_size_files = glob.glob("./test_liner_0416_mid/log/save_best_len_log/*")
    cell_size_files = glob.glob("./graphDrawing/data/my_algorithm/liner_networkx_0508_mid_20/log/save_best_len_log/*")
    cell_size_files = glob.glob("./graphDrawing/data/egraph/liner_egraph_networkx_20/log/save_best_len_log/*")
    # cell_size_files = glob.glob("./ pacificvis2024_log/suiteSparse/honban_random_liner_detail/log/save_best_len_log/*")
    # cell_size_files = glob.glob("./ pacificvis2024_log/suiteSparse/honban_random_liner_detail/log/save_best_len_log/*")

    plt_x = []
    plt_y = []


    for filepath in cell_size_files:
        if os.path.isdir(filepath):
            continue
        with open(filepath) as f:
            data = json.load(f)
        file_name = re.split('[/.-]', filepath)[7]
        # print(file_name)

        # if file_name=="octahedral" or file_name=="cubical" or file_name=="frucht":
        # if file_name!="octahedral":
        #     continue

        # typeA, Dは省く
        if file_name in graph_info["Networkx"] and  (graph_info["Networkx"][file_name]["type"] == "a" or graph_info["Networkx"][file_name]["type"] == "d"):
        # if file_name in graph_info["SuiteSparse Matrix"] and  (graph_info["SuiteSparse Matrix"][file_name]["type"] == "a" or graph_info["SuiteSparse Matrix"][file_name]["type"] == "d"):
            continue

        obj = get_stress(data, file_name)
       
        plt_x.append(obj["x"])
        plt_y.append(obj["y"])

    # exit()

    # 散布図描画
    # sns.scatterplot(
    #     x=reduce(lambda a, b: a + b, plt_x), y=reduce(lambda a, b: a + b, plt_y))
    sns.boxplot(
        x=reduce(lambda a, b: a + b, plt_x), y=reduce(lambda a, b: a + b, plt_y), color="white", showfliers=False)
    
    plt.ylim(bottom=1.0)
    plt.axhline(y=1.1)
    plt.axhline(y=1.05, color="r")

    plt.show()

    print(reduce(lambda a, b: a + b, plt_x))
        
    

if __name__ == '__main__':
    main()



