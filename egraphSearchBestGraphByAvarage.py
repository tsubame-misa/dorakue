import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import torusSGD, egraphTorusSGD
from common import drawGraph, log, initGraph
import re
import matplotlib.pyplot as plt
import math
import os
import shutil

"""
torusでstressを最も低くするlenghtを求める
(maxdを何倍したものがstressが低くなるか)
"""


def get_midium_graph(graph, file_name, multiple_num, loop_value=20):
    """
    return ストレスの平均, 中央値を取るグラフ, bestなグラフ, bestなグラフのid
    """
    all_log = dict()
    stress = []
    for j in range(loop_value):
        time = setup.get_time()
        index_time = str(j) + str(time)
        _log =  egraphTorusSGD.torus_sgd(graph, file_name, multiple_num, j, index_time)
        all_log[index_time] = _log
        stress.append([index_time, _log["stress"]])

    sorted_stress = sorted(stress,  key=lambda x: x[1])
    stress_sum = sum([x[1] for x in stress])
    return stress_sum/loop_value, all_log[sorted_stress[len(sorted_stress)//2][0]], all_log[sorted_stress[0][0]], sorted_stress[0][0] 

def show_stress_graph(x, y, file_name):
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(x, y, marker='o',
             label='stress', linestyle='-', color='r')
    
    # ラベルやタイトルの設定
    plt.xlabel('How many times maxd')
    plt.title(file_name)
    plt.legend()  # 凡例を表示

    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/stress_by_len/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_path = './' + dir_name+'/stress_by_len/' + file_name+'.png'
    plt.savefig(img_path)


def save_best_graph(best_graph_time, best_log, file_name, multipl_number):
    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/best/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    # 画像の保存
    new_dir_path = './' + dir_name + "/best/img" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_file_name = file_name + "-" + str(multipl_number) + "-" + best_graph_time + ".png"
    
    shutil.copyfile(dir_name + "/torusSGD_wrap/" + img_file_name, new_dir_path+ "/" + img_file_name)  
    print("saved", new_dir_path+ "/" + img_file_name)

    # ログの保存
    best_log["multipl_number"] = multipl_number
    log.create_log(best_log, file_name+"-best")

def search_min_stress_len(graph, file_name, loop=20, log_file_name="test"):
    low = 0
    high = 3

    lr_diff = high-low
    x = (3-math.sqrt(5))/2*lr_diff
    low_multipl_number = x
    high_multipl_number = high - x

    low_graph_stress, low_graph, low_best_graph, low_best_graph_time = get_midium_graph(graph, file_name, low_multipl_number, loop)
    high_graph_stress,  high_graph, high_best_graph, high_best_graph_time = get_midium_graph(graph, file_name, high_multipl_number, loop)

    data = []
    all_log = {"file": file_name}
    
    i = 0
    while abs(low_multipl_number-high_multipl_number) >= 0.001:
        i += 1
        print(i, low, high)
        """
        計算量をなんとかしたい
        1. ここを中央値にする(最低ライン)
        2. 広い領域で描画した結果を狭い領域での描画に使いまわしたい(逆も)
         - 初期配置を、前のものを使う
         - 連続性を期待するため、中央値は取らない。一回だけやる
         - 3分に限らずでも
        """
            
        if low_graph_stress > high_graph_stress:
            data.append([low_multipl_number, low_graph["stress"]])
            all_log[low_multipl_number] = {"1":{"torusSGD":low_graph, "avarage":low_graph_stress}}

            low = low_multipl_number
            low_multipl_number = high_multipl_number
            high_multipl_number = high - (lr_diff-2*x)

            low_graph_stress = high_graph_stress
            low_graph = high_graph
            low_best_graph_time = high_best_graph_time    
            high_graph_stress, high_graph, high_best_graph, high_best_graph_time = get_midium_graph(graph, file_name, high_multipl_number, loop)
        else:
            data.append([high_multipl_number, high_graph["stress"]])
            all_log[high_multipl_number] = {"2":{"torusSGD":high_graph, "avarage":high_graph_stress}}

            high = high_multipl_number
            high_multipl_number = low_multipl_number
            low_multipl_number = low + lr_diff-2*x

            high_graph_stress = low_graph_stress
            high_graph = low_graph
            high_best_graph_time = low_best_graph_time
            low_graph_stress, low_graph, low_best_graph, low_best_graph_time = get_midium_graph(graph, file_name, low_multipl_number, loop)
        
        lr_diff = high-low
        x = (3-math.sqrt(5))/2*lr_diff
    
    if low_graph_stress > high_graph_stress:
        print("min", high_multipl_number)
        all_log["best"] = high_best_graph
        save_best_graph(high_best_graph_time, high_best_graph, file_name, high_multipl_number)
    else:
        print("min", low_multipl_number)
        all_log["best"] = low_best_graph
        save_best_graph(low_best_graph_time, low_best_graph, file_name, low_multipl_number)

    sorted_data = sorted(data, key=lambda x: x[0])

    log.create_log(all_log, file_name)

    show_stress_graph([row[0] for row in sorted_data],[row[1] for row in sorted_data], file_name)

    if low_graph_stress > high_graph_stress:
        return high_best_graph
    else:
        return low_best_graph


def main():
    # files = glob.glob("./graph_networkx_only/*")
    # files = glob.glob("./scallFreeGraph2/*")
    # files = glob.glob("./dwtGraph/*")
    # files = glob.glob("./chen2021Graph/*")
    # files = glob.glob("./chen2021Graph2/*")
    # files = glob.glob("./randomGraphs/*")
    files = glob.glob("./doughNetGraph/default/*")

    # 使用するグラフをノード数順に並び替える
    graphs = []
    for filepath in files:
        if filepath[-3:]=="txt":
            continue
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/.]', filepath)[4]
        # file_name = re.split('[/]', filepath)[2][:-5]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    
    # log_file_name = "search_by_avarage_15_20"
    # log_file_name = "test_0102_honban_3_20_20loop_2"
    log_file_name = "uuu_test"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        if not g["name"]=="10":
            continue
        print(g["name"], "size", len(g["graph"].nodes))
        search_min_stress_len(g["graph"], g["name"], 1)
       


if __name__ == '__main__':
    main()