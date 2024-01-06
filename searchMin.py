import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import egraphTorusSGD
from common import drawGraph, log
import re
import matplotlib.pyplot as plt
import os
import math

"""
lenの変化でstessがどう変わるか線形探索
"""

# COUNT = 30
COUNT = 80

def create_graph(graph, file_name, multiple_num, i):
    time = setup.get_time()
    index_time = str(i) + str(time)
    drawGraph.set_time(index_time)
    torus_log = egraphTorusSGD.torus_sgd(graph,file_name, multiple_num, i, index_time)
    return torus_log


def show_stress_graph(x, y, file_name, dir_name):
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(x, y, marker='',
             label='stress', linestyle='-', color='r', )
    
    # ラベルやタイトルの設定
    plt.xlabel('How many times maxd')
    plt.ylabel('stress')
    plt.title(file_name)
    plt.legend()  # 凡例を表示

    new_dir_path = './' + dir_name + "/stress_by_len/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_path = './' + dir_name+'/stress_by_len/' + file_name+'.png'
    plt.savefig(img_path)
    print(img_path)

    plt.clf()
    plt.close()

def show_stress_compare_graph(x, torus_y, no_torus_y,  file_name, dir_name):
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(x, torus_y, marker='',
             label='stress', linestyle='-', color='r', )
    plt.plot(x, no_torus_y, marker='',
             label='stress', linestyle='-', color='b', )
    
    # ラベルやタイトルの設定
    plt.xlabel('How many times diamater')
    plt.ylabel('stress')
    plt.title(file_name)
    plt.legend()  # 凡例を表示

    new_dir_path = './' + dir_name + "/stress_by_len_compare/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_path = './' + dir_name+'/stress_by_len_compare/' + file_name+'.png'
    plt.savefig(img_path)
    print(img_path)

    plt.clf()
    plt.close()


def save_best_len_log(best_multiple_num, best_stress_comp, x, y, torus, file_name):
    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/log/save_best_len_log/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    best_log = {"best_multiple_num": best_multiple_num, "best_stress_comp":best_stress_comp, 
                "x":x , "y":y, "torus_y":torus, "file_name":file_name}
    log.create_log(best_log, "save_best_len_log/"+file_name)
    

def get_stress_by_len(graph, file_name, idx):
    data = []
    all_log = {"file": file_name}
    for i in range(1, COUNT+1):
        n = math.floor(i*0.05*100)/100
        # n = math.floor(i*0.1*100)/100
        torus_log= create_graph(graph, file_name, n, idx)
        data.append([n, torus_log["stress"]])
        all_log[n] = {"1":{"torusSGD":torus_log}}
    
    sorted_data = sorted(data, key=lambda x: x[0])

    log.create_log(all_log, file_name)
    return [row[0] for row in sorted_data],[row[1] for row in sorted_data]


def generate_stress_liner_graph(graph, file_name, dir_name):
    torus_data = [[] for i in range(COUNT)]
    x = []
    y = []
    torus = []
    for i in range(20): 
        print(i)
        key, torus_value = get_stress_by_len(graph, file_name, i)
        x = key
        for j in range(len(torus_value)):
            torus_data[j].append(torus_value[j])
    
    for j in range(len(torus_data)):
        torus_sorted_d = sorted(torus_data[j])
        torus_y = torus_sorted_d[len(torus_sorted_d)//2]
        # お試し
        torus_sum = sum(torus_data[j])
        torus_y = torus_sum/len(torus_sorted_d)

        y.append(torus_y) 
        torus.append(torus_y)
    
    print(x)
    print(y)
    show_stress_graph(x, y, file_name, dir_name)
    # show_stress_compare_graph(x, torus, no_torus, file_name, dir_name)

    best_stress_comp = min(y)
    best_idx = y.index(best_stress_comp)
    best_multiple_num = x[best_idx]
    save_best_len_log(best_multiple_num, best_stress_comp, x, y, torus, file_name)
   


def main():
    # files = glob.glob("./graph/*")
    # files = glob.glob("./chen2021Graph/*")
    # files = glob.glob("./scallFreeGraph2/*")
    # files = glob.glob("./dwtGraph/*")
    files = glob.glob("./doughNetGraph/default/*")
    # files = glob.glob("./randomGraphs/*")
    
    graphs = []
    for filepath in files:
        if filepath[-3:]=="txt" or filepath[-4:]=="test":
            continue
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/.]', filepath)[4]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)


    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    log_file_name = "test_stress_liner_avarage_20_20loop"
    log_file_name = "uuu_chen2020_liner"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        if not g["name"] in ["07", "10", "15"]:
            continue
        print(g["name"], "size", len(g["graph"].nodes))
        generate_stress_liner_graph(g["graph"], g["name"], log_file_name)
        print("---------------------")


if __name__ == '__main__':
    main()
