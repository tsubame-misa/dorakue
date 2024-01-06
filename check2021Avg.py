"""
黄金探索とchenらのグラフ生成と比較までがセット
"""


import json
import setup
from common import log,  drawGraph 
import egraphSearchBestGraphByAvarage
import chenTorus
import glob
from networkx.readwrite import json_graph
import json
import setup
from common import drawGraph, log
import re


def check(scale_free_graph, name):
    box_data = dict()

    time = setup.get_time()
    index_time = str(0) + str(time)
    drawGraph.set_time(index_time)
    chen_log, _time=  chenTorus.get_best_graph(scale_free_graph, name+"chen")
    chenTorus.save_best_graph(_time, chen_log, name+"chen")
    our_log = egraphSearchBestGraphByAvarage.search_min_stress_len(scale_free_graph, name)
    print(chen_log)

    for k in ["edge_length_variance","minimum_angle", "edge_crossings", "stress", "node_resolution"]:
        if k=="edge_crossings":
            v = (chen_log["edge_crossings"]+1)/(our_log["edge_crossings"]+1) 
        else:
            v = chen_log[k]/our_log[k]
        box_data[k] = v

    print(box_data)
    save_log ={"ratio":box_data,"our":our_log, "chen":chen_log}
    log.create_log(save_log, "comp-"+ name)



files = glob.glob("./chen2021Graph/use/*")
graphs = []
for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    file_name = re.split('[/]', filepath)[3][:-5]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)


sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
log_file_name = "uuu_check2021"
setup.set_dir_name(log_file_name)
log.create_log_folder()

for g in sorted_graphs:
    print(g["name"], "size", len(g["graph"].nodes))
    check(g["graph"], g["name"])
    print("---------------------")
