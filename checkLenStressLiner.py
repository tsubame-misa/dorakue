import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import SGD, torusSGD
from common import drawGraph, log, initGraph
import re
import matplotlib.pyplot as plt
import os

"""
lenの変化でstessがどう変わるか
"""

COUNT = 100

def create_graph(graph, file_name, multiple_num, maxd, i):
    _len = multiple_num*maxd
    time = setup.get_time()
    index_time = str(i) + str(time)
    drawGraph.set_time(index_time)
    torus_log = torusSGD.torus_sgd(graph, file_name, _len, _len)
    sgd_log = SGD.sgd(graph, file_name, _len, _len)
    return torus_log, sgd_log


def show_stress_graph(x, y, file_name, dir_name):
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(x, y, marker='',
             label='stress', linestyle='-', color='r', )
    
    # ラベルやタイトルの設定
    plt.xlabel('How many times maxd')
    plt.ylabel('What percentage of no-torus is better')
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
    plt.xlabel('How many times maxd')
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


def save_best_len_log(best_multiple_num, best_stress_comp, x, y, torus, no_torus,  file_name):
    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/log/save_best_len_log/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    best_log = {"best_multiple_num": best_multiple_num, "best_stress_comp":best_stress_comp, 
                "x":x , "y":y, "torus_y":torus, "no_torus_y":no_torus, "file_name":file_name}
    log.create_log(best_log, "save_best_len_log/"+file_name)
    

def get_stress_by_len(graph, file_name):
    data = []

    all_log = {"file": file_name}

    setup.init()
    setup.set_dir_name(log_file_name)
    maxd = initGraph.get_maxd(graph, file_name)
    initGraph.get_pos(len(graph.nodes()), maxd, maxd)
    
    for i in range(1, COUNT+1):
        n = i*0.05
        time = setup.get_time()
        index_time = str(i) + str(time)

        torus_log, sgd_log= create_graph(graph, file_name, n, maxd, index_time)
        
        data.append([n, torus_log["stress"], sgd_log["stress"]])
        all_log[maxd*n] = {"1":{"torusSGD":torus_log, "sgd_log":sgd_log}}
    
    sorted_data = sorted(data, key=lambda x: x[0])

    log.create_log(all_log, file_name)
    return [row[0] for row in sorted_data],[row[1] for row in sorted_data], [row[2] for row in sorted_data]


def generate_stress_liner_graph(graph, file_name, dir_name):
    torus_data = [[] for i in range(COUNT)]
    sgd_data = [[] for i in range(COUNT)]
    x = []
    y = []
    torus = []
    no_torus = []
    for i in range(50): 
        print(i)
        key, torus_value, sgd_value = get_stress_by_len(graph, file_name)
        x = key
        for j in range(len(torus_value)):
            torus_data[j].append(torus_value[j])
            sgd_data[j].append(sgd_value[j])
    
    for j in range(len(torus_data)):
        torus_sorted_d = sorted(torus_data[j])
        sgd_sorted_d = sorted(sgd_data[j])

        torus_y = torus_sorted_d[len(torus_sorted_d)//2]
        sgd_y = sgd_sorted_d[len(sgd_sorted_d)//2]
        # print(torus_y, sgd_y, sgd_y/torus_y)
        # 何倍よくなっているか
        y.append(sgd_y/torus_y) #1000/100 = 10
        torus.append(torus_y)
        no_torus.append(sgd_y)
    
    show_stress_graph(x, y, file_name, dir_name)
    # show_stress_compare_graph(x, torus, no_torus, file_name, dir_name)

    best_stress_comp = min(y)
    min_y_idx = y.index(best_stress_comp)
    best_multiple_num = x[min_y_idx]
    save_best_len_log(best_multiple_num, best_stress_comp, x, y, torus, no_torus, file_name)
   
    

files = glob.glob("./graph/*")
graphs = []

for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    file_name = re.split('[/.]', filepath)[3]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)


sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
log_file_name = "result_graph_stress_liner"
setup.set_dir_name(log_file_name)
log.create_log_folder()


for g in sorted_graphs:
    print(g["name"], "size", len(g["graph"].nodes))
    generate_stress_liner_graph(g["graph"], g["name"], log_file_name)
    print("---------------------")
