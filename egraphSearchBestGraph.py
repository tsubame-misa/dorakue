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

def create_graph(graph, file_name, multiple_num, maxd, i):
    _len = multiple_num*maxd
    time = setup.get_time()
    index_time = str(i) + str(time)
    drawGraph.set_time(index_time)
    _log = torusSGD.torus_sgd(graph, file_name, _len, _len, multiple_num)
    return _log


def get_midium_graph(graph, file_name, multiple_num, loop_value=10):
    """
    return 中央値を取るグラフ, bestなグラフ, bestなグラフのid
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
    return all_log[sorted_stress[len(sorted_stress)//2][0]], all_log[sorted_stress[0][0]], sorted_stress[0][0] 

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

def search_min_stress_len(graph, file_name, log_file_name="test"):
    count = 20

    low = 0
    high = 5

    lr_diff = high-low
    x = (3-math.sqrt(5))/2*lr_diff
    low_multipl_number = x
    high_multipl_number = high - x

    low_graph, low_best_graph, low_best_graph_time = get_midium_graph(graph, file_name, low_multipl_number)
    high_graph, high_best_graph, high_best_graph_time = get_midium_graph(graph, file_name, high_multipl_number)

    data = []
    all_log = {"file": file_name}
    
    for i in range(1, count):
        print(i, low, high)
        """
        計算量をなんとかしたい
        1. ここを中央値にする(最低ライン)
        2. 広い領域で描画した結果を狭い領域での描画に使いまわしたい(逆も)
         - 初期配置を、前のものを使う
         - 連続性を期待するため、中央値は取らない。一回だけやる
         - 3分に限らずでも
        """
            
        if low_graph["stress"] > high_graph["stress"]:
            data.append([low_multipl_number, low_graph["stress"]])
            all_log[low_multipl_number] = {"1":{"torusSGD":low_graph}}

            low = low_multipl_number
            low_multipl_number = high_multipl_number
            high_multipl_number = high - (lr_diff-2*x)

            low_graph = high_graph
            low_best_graph_time = high_best_graph_time    
            high_graph, high_best_graph, high_best_graph_time = get_midium_graph(graph, file_name, high_multipl_number)
        else:
            data.append([high_multipl_number, high_graph["stress"]])
            all_log[high_multipl_number] = {"2":{"torusSGD":high_graph}}

            high = high_multipl_number
            high_multipl_number = low_multipl_number
            low_multipl_number = low + lr_diff-2*x

            high_graph = low_graph
            high_best_graph_time = low_best_graph_time
            low_graph, low_best_graph, low_best_graph_time = get_midium_graph(graph, file_name, low_multipl_number)
        
        lr_diff = high-low
        x = (3-math.sqrt(5))/2*lr_diff
        
        if abs(low_multipl_number-high_multipl_number) < 0.0001:
            break
    
    if low_graph["stress"] > high_graph["stress"]:
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


def main():
    files = glob.glob("./graph/*")
    # files = glob.glob("./scallFreeGraph2/*")
    # files = glob.glob("./dwtGraph/*")

    # 使用するグラフをノード数順に並び替える
    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/.]', filepath)[3]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    
    log_file_name = "test"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        if len(g["graph"].nodes) < 30:
            continue
        print(g["name"], "size", len(g["graph"].nodes))
        search_min_stress_len(g["graph"], g["name"], log_file_name)


if __name__ == '__main__':
    main()