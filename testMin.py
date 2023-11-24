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

COUNT = 60

def create_graph(graph, file_name, multiple_num, maxd, i):
    _len = multiple_num*maxd
    time = setup.get_time()
    index_time = str(i) + str(time)
    drawGraph.set_time(index_time)
    # SGD.sgd(graph, file_name, _len, _len)
    # _log = torusSGD.torus_sgd(graph, file_name, _len, _len, multiple_num)

    setup.init()
    _log = torusSGD.torus_sgd(graph, file_name, _len, _len)

    # drawGraph.create_compare_fig(file_name)
    # _log = log.get_log()

    return _log


def show_stress_graph(x, y, file_name, dir_name):
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(x, y, marker='',
             label='stress', linestyle='-', color='r', )
    
    # ラベルやタイトルの設定
    plt.xlabel('How many times maxd')
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



def get_stress_by_len(graph, file_name):
    maxd = initGraph.get_maxd(graph, file_name)

    data = []

    all_log = {"file": file_name}

    setup.init()
    # 初期配置を揃えてストレスの計算をするべきなのでは？
    # maxd*時を起点にしてあとは倍にする？
    initGraph.get_pos(len(graph.nodes()), maxd, maxd)
    setup.set_dir_name(log_file_name)

    n = 0
    
    for i in range(COUNT):
        n += 0.05
        time = setup.get_time()
        index_time = str(i) + str(time)

        _graph= create_graph(graph, file_name, n, maxd, index_time)

        # print(n,n*maxd, _graph["stress"])
        
        data.append([n, _graph["stress"]])
        all_log[maxd*n] = {"1":{"torusSGD":_graph}}
    
    sorted_data = sorted(data, key=lambda x: x[0])

    log.create_log(all_log, file_name)
    # show_stress_graph([row[0] for row in sorted_data],[row[1] for row in sorted_data], file_name)
    return [row[0] for row in sorted_data],[row[1] for row in sorted_data]


def test(graph, file_name, dir_name):
    data = [[] for i in range(COUNT)]
    x = []
    y = []
    for i in range(50): 
        print(i)
        key, value = get_stress_by_len(graph, file_name)
        x = key
        for j in range(len(value)):
            data[j].append(value[j])
    
    for d in data:
        sorted_d = sorted(d)
        y.append(sorted_d[len(sorted_d)//2])
    
    show_stress_graph(x, y, file_name, dir_name)
    




files = glob.glob("./graph/*")
graphs = []

for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    file_name = re.split('[/.]', filepath)[3]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)


sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
log_file_name = "result"
setup.set_dir_name(log_file_name)
log.create_log_folder()

graph_names = ["dodecahedral"]
graph_names = ["hoffman_singleton",
               "dodecahedral", "florentine_families", "moebius_kantor"]
# graph_names = ["hoffman_singleton", "chvatal", "icosahedral",
            #    "dodecahedral", "florentine_families", "moebius_kantor"]

for g in sorted_graphs:
    if not g["name"] in graph_names:
        continue
    print(g["name"], "size", len(g["graph"].nodes))
    test(g["graph"], g["name"], log_file_name)
    print("---------------------")
