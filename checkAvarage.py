"""
中央値だとlinerが変わらなくてなんで？ってなってて平均で試してみようってなった残骸な気がしてる
"""
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


def get_avg(graph, file_name, multiple_num, loop_value=5):
    """
    return ストレスの平均, 中央値を取るグラフ, bestなグラフ, bestなグラフのid
    """
    stress = []
    for j in range(loop_value):
        time = setup.get_time()
        index_time = str(j) + str(time)
        _log =  egraphTorusSGD.torus_sgd(graph, file_name, multiple_num, j, index_time)
        stress.append([index_time, _log["stress"]])

    stress_sum = sum([x[1] for x in stress])
    return stress_sum/loop_value


def get_midium_graph(graph, file_name, multiple_num, loop_value=5):
    """
    return ストレスの平均, 中央値を取るグラフ, bestなグラフ, bestなグラフのid
    """
    stress = []
    for j in range(loop_value):
        time = setup.get_time()
        index_time = str(j) + str(time)
        _log =  egraphTorusSGD.torus_sgd(graph, file_name, multiple_num, j, index_time)
        stress.append([index_time, _log["stress"]])

    sorted_stress = sorted(stress,  key=lambda x: x[1])
    return sorted_stress[len(sorted_stress)//2][0] 


def show_stress_graph(x, y, file_name):
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(x, y, marker='o',
             label='stress', linestyle='-', color='r')
    
    # ラベルやタイトルの設定
    plt.xlabel('loop')
    plt.title(file_name)
    plt.legend()  # 凡例を表示

    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/check_mid/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_path = './' + dir_name+'/check_mid/' + file_name+'.png'
    plt.savefig(img_path)


def search_min_stress_len(graph, file_name, log_file_name="test"):
    x = []
    y = []
    for i in range(0, 50, 5):
        if i==0:
            continue
        print(i)
        # graph_stress = get_avg(graph, file_name, 1, i)
        graph_stress = get_midium_graph(graph, file_name, 1.5, i)
        
        x.append(i)
        y.append(graph_stress)
    show_stress_graph(x, y, file_name)


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
    
    # log_file_name = "search_by_avarage_15_20"
    log_file_name = "uuuu"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    priprity = ["cubical", "tutte", "frucht", "heawood", "moebius_kantor", "pappus" "dodecahedral"]

    for g in sorted_graphs:
        # if not g["name"] == "dodecahedral":
        if not g["name"] in priprity:
            continue
        print(g["name"], "size", len(g["graph"].nodes))
        search_min_stress_len(g["graph"], g["name"], log_file_name)
        exit()


if __name__ == '__main__':
    main()