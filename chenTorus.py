import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import egraphTorusSGD 
from common import drawGraph, log
import re
import os
import shutil
import matplotlib.pyplot as plt
import networkx as nx

"""
各グラフに対してn個描画し、ストレスが中央値のものを代表として保存
"""

def generate_box_plot(data,file_name):
    # 箱ひげ図の描画
    plt.boxplot(data)

    # グリッドを表示
    plt.grid(True)

    # グラフのタイトルと軸ラベル
    plt.title(file_name + " min:" + str(data[0]))
    plt.xlabel('')
    plt.ylabel('stress')

    # 箱ひげ図を表示
    # plt.show()

    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/box_plot/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_path = './' + dir_name+'/box_plot/' + file_name+'.png'
    plt.savefig(img_path)
    print(img_path)

    plt.clf()
    plt.close()


def get_best_graph(graph, file_name, loop_value=1):
    all_log = dict()
    stress = []
    for j in range(loop_value):
        print(j)
        time = setup.get_time()
        index_time = str(j) + str(time)
        drawGraph.set_time(index_time)
        _log =  egraphTorusSGD.torus_sgd(graph, file_name, 1, j, index_time, True)
        all_log[index_time] = _log
        stress.append([index_time, _log["stress"]])
    sorted_stress = sorted(stress,  key=lambda x: x[1])
    # generate_box_plot([x[1] for x in sorted_stress], file_name)
    return all_log[sorted_stress[0][0]], sorted_stress[0][0] 


def save_best_graph(best_graph_time, best_log, file_name):
    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/best/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    # 画像の保存
    new_dir_path = './' + dir_name + "/best/img" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_file_name = file_name + "-" + str(best_log["multiple_num"]) +"-" + best_graph_time + ".png"
    
    shutil.copyfile(dir_name + "/torusSGD_wrap/" + img_file_name, new_dir_path+ "/" + img_file_name)  
    print("saved", new_dir_path+ "/" + img_file_name)

    log.create_log(best_log, file_name+"-best")


def generate_graph(graph, file_name):
    _graph, time = get_best_graph(graph, file_name)
    save_best_graph(time, _graph, file_name)


def main():
    # files = glob.glob("./graph/*")
    # files = glob.glob("./scallFreeGraph2/*")
    files = glob.glob("./randomGraphs/*")
    # files = glob.glob("./doughNetGraph/default/*")
    # files = glob.glob("./chen2021Graph/*")
   
    graphs = []
    for filepath in files:
        if filepath[-3:]=="txt":
            continue
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/.]', filepath)[3]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    
    log_file_name = "random_graph_test_chen"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        print(g["name"], "size", len(g["graph"].nodes))
        if len(g["graph"].nodes) < 800:
            continue
        generate_graph(g["graph"], g["name"])
        print("---------------------")

if __name__ == '__main__':
    main()
