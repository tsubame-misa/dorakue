import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import SGD, torusSGD
from common import drawGraph, log, initGraph
import re
import matplotlib.pyplot as plt



"""
torusでstressを最も低くするlenghtを求める
(maxdを何倍したものがstressが低くなるか)
"""


def create_graph(graph, file_name, multiple_num, maxd, i):
    _len = multiple_num*maxd
    time = setup.get_time()
    index_time = str(i) + str(time)
    drawGraph.set_time(index_time)
    # SGD.sgd(graph, file_name, _len, _len)
    _log = torusSGD.torus_sgd(graph, file_name, _len, _len, multiple_num)
    # drawGraph.create_compare_fig(file_name)
    # _log = log.get_log()

    return _log


def get_midium_graph(graph, file_name, multiple_num, maxd, i, loop_value=25):
    for j in range(loop_value):
        _len = multiple_num*maxd
        time = setup.get_time()
        index_time = str(i) + str(time)
        drawGraph.set_time(index_time)
        _log = torusSGD.torus_sgd(graph, file_name, _len, _len, multiple_num)
        return _log


def show_stress_graph(x, y, file_name):
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(x, y, marker='o',
             label='stress', linestyle='-', color='r')
    
    # ラベルやタイトルの設定
    plt.xlabel('How many times maxd')
    plt.title(file_name)
    plt.legend()  # 凡例を表示

    plt.show()



def search_min_stress_len(graph, file_name):
    maxd = initGraph.get_maxd(graph, file_name)
    count = 10

    low = 0
    high = 5

    data = []

    all_log = {"file": file_name}

    setup.init()
    initGraph.get_pos(len(graph.nodes()), maxd, maxd)
    setup.set_dir_name(log_file_name)
    
    for i in range(count):
        low_multipl_number = (low * 2 + high) / 3
        high_multipl_number = (low + high * 2) / 3

        time = setup.get_time()
        index_time = str(i) + str(time)

        """
        計算量をなんとかしたい
        1. ここを中央値にする(最低ライン)
        2. 広い領域で描画した結果を狭い領域での描画に使いまわしたい(逆も)
         - 初期配置を、前のものを使う
         - 連続性を期待するため、中央値は取らない。一回だけやる
         - 3分に限らずでも
        """
        low_graph= create_graph(graph, file_name, low_multipl_number, maxd, index_time)
        high_graph = create_graph(graph, file_name, high_multipl_number, maxd, index_time)

        # print(low, high, min(low_graph["stress"] , high_graph["stress"]))
        # print(low_multipl_number,low_graph["stress"],"|", high_multipl_number, high_graph["stress"])
        # exit()

        if low_graph["stress"] > high_graph["stress"]:
            low = low_multipl_number
            data.append([low_multipl_number, low_graph["stress"]])
            all_log[maxd*low_multipl_number] = {"1":{"torusSGD":low_graph}}
        else:
            high = high_multipl_number
            data.append([high_multipl_number, high_graph["stress"]])
            all_log[maxd*high_multipl_number] = {"2":{"torusSGD":high_graph}}
        
        if abs(low_graph["stress"] - high_graph["stress"]) < 1 or abs(maxd*low_multipl_number-maxd*high_multipl_number) < 1:
        # if abs(high - low) < 1e-5:
            break
    
    print()
    if low_graph["stress"] > high_graph["stress"]:
        print("min", high_multipl_number, maxd*high_multipl_number)
    else:
        print("min", low_multipl_number, maxd*low_multipl_number)

    sorted_data = sorted(data, key=lambda x: x[0])

    log.create_log(all_log, file_name)
    # print(sorted_data)
    # print()
    # print([row[0] for row in sorted_data])
    # print([row[1] for row in sorted_data])


    show_stress_graph([row[0] for row in sorted_data],[row[1] for row in sorted_data], file_name)


    
        






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

# graph_names = ["hoffman_singleton", "chvatal", "icosahedral",
#                "dodecahedral", "florentine_families", "moebius_kantor"]
graph_names = ["dodecahedral"]

for g in sorted_graphs:
    if not g["name"] in graph_names:
        continue
    print(g["name"], "size", len(g["graph"].nodes))
    search_min_stress_len(g["graph"], g["name"])
    print("---------------------")
