
import glob
from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt
import csv
import matplotlib.pyplot as plt
import seaborn as sns

"""
タイプB,CのグラフでTypeAにみなせるものがあるかを調べる
"""


def main():
    files = glob.glob("./graphSet/networkx/*")

    cell_size_info = {}
    cell_size_files = glob.glob("./test_liner_egraph_networkx_20/log/save_best_len_log/*")
    cell_size_files = glob.glob("./graphDrawing/data/egraph/liner_egraph_networkx_20/log/save_best_len_log/*")

    with open("./graphSet/info202405_egraph.json") as f:
        graph_info = json.load(f)

    
    for filepath in cell_size_files:
        with open(filepath) as f:
            data = json.load(f)
        file_name = re.split('[/.-]', filepath)[8]
        if graph_info["Networkx"][file_name]["type"] == "a" or graph_info["Networkx"][file_name]["type"] == "d":
            continue

        # if not(file_name=="house" or file_name=="house_x" or file_name=="tutte"):
        #     continue

        print(file_name,graph_info["Networkx"][file_name]["type"])
        print("min_stress/no_torus_stress", data["best_stress_comp"]/data["y"][-1], "min_stress",data["best_stress_comp"], "no_torus_stress", data["y"][-1])
        # print(abs(data["best_stress_comp"]-data["y"][-1])/data["y"][-1])
        print()

        plt.figure(figsize=(8, 6))  # グラフのサイズを設定
        plt.plot(data["x"][20:-10], data["y"][20:-10], marker='',
                label='stress', linestyle='-', color='r', )
        # ラベルやタイトルの設定
        plt.xlabel('How many times maxd')
        plt.ylabel('stress')
        plt.ylim(bottom=0)
        plt.title(file_name)
        plt.legend()  # 凡例を表示
        # plt.show()
        
if __name__ == '__main__':
    main()