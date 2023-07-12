import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.kamadaKawaiBase import kameKame, torusKameCenter
from algorithm.SGDBase import SGD, torusSGD
from common import drawGraph, log, initGraph
import re


def create_graph(graph, file_name):
    maxd = initGraph.get_maxd(graph, file_name)
    len_list = [maxd, maxd*(2**0.5), maxd*2]
    all_log = {"file": file_name}
    for _len in len_list:
        width = _len
        height = _len
        wh_log = {}
        term = setup.get_term()
        # term = 1
        for i in range(term):
            setup.init()
            time = setup.get_time()
            drawGraph.set_time(time)
            SGD.sgd(graph, file_name, width, height)
            torusSGD.torus_sgd(graph, file_name, width, height)
            kameKame.kamada_kawai(graph, file_name, width, height)
            torusKameCenter.torus_kame(graph, file_name, width, height)
            drawGraph.create_compare_fig(file_name)
            _log = log.get_log()
            wh_log[str(time)] = _log

            message = str(time)
            print(message)

        all_log[str(_len)] = wh_log

    log.clear()
    time = setup.get_time()
    log.create_log(all_log, file_name)


files = glob.glob("./graph/*")
graphs = []

for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    # file_name = filepath.split("/")[-1]
    file_name = re.split('[/.]', filepath)[3]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)


sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

for g in sorted_graphs:
    print(g["name"], "size", len(g["graph"].nodes))
    setup.set_term(1)
    create_graph(g["graph"], g["name"])
    print("---------------------")
