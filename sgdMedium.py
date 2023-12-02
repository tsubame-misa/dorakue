import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import SGD
from common import drawGraph, log, initGraph
import re
import os
import shutil

"""
各グラフに対してn個描画し、ストレスが中央値のものを代表として保存
"""

def get_midium_graph(graph, file_name, loop_value=50):
    all_log = dict()
    stress = []
    for j in range(loop_value):
        # print("get midium", j)
        time = setup.get_time()
        index_time = str(j) + str(time)
        drawGraph.set_time(index_time)
        _log = SGD.sgd(graph, file_name)
        all_log[index_time] = _log
        stress.append([index_time, _log["stress"]])

    sorted_stress = sorted(stress,  key=lambda x: x[1])
    return all_log[sorted_stress[len(sorted_stress)//2][0]], sorted_stress[len(sorted_stress)//2][0] 


def save_best_graph(best_graph_time, best_log, file_name, _len):
    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/best/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    # 画像の保存
    new_dir_path = './' + dir_name + "/best/img" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_file_name = file_name + "-" + str(_len) + "-" + best_graph_time + ".png"
    
    shutil.copyfile(dir_name + "/SGD/" + img_file_name, new_dir_path+ "/" + img_file_name)  
    print("saved", new_dir_path+ "/" + img_file_name)

    # ログの保存
    best_log["len"] = _len
    log.create_log(best_log, file_name+"-best")


def search_min_stress_len(graph, file_name):
    setup.init()
    setup.set_dir_name(log_file_name)
    maxd = initGraph.get_maxd(graph, file_name)
    _graph, time = get_midium_graph(graph, file_name)
    save_best_graph(time, _graph, file_name, maxd)
    

files = glob.glob("./graph/*")
graphs = []

for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    file_name = re.split('[/.]', filepath)[3]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)

sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
log_file_name = "result1125_sgd"
setup.set_dir_name(log_file_name)
log.create_log_folder()

for g in sorted_graphs:
    print(g["name"], "size", len(g["graph"].nodes))
    search_min_stress_len(g["graph"], g["name"])
    print("---------------------")
