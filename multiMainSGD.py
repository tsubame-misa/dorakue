import json
from networkx.readwrite import json_graph
from algorithm.SGDBase import SGD, torusSGD
from common import log, drawGraph
import setup


filename = './graph/les_miserables.json'
print(filename)
graph = json_graph.node_link_graph(json.load(open(filename)))

all_log = {"file": filename}


def create_sgd_graph(graph, filename):
    len_list = setup.get_len()
    all_log = {"file": filename}
    print("SGD")
    for _len in len_list:
        width = _len
        height = _len
        wh_log = {}
        print(_len)
        term = setup.get_term()
        for i in range(term):
            setup.init()
            setup.set_roop1(50)

            time = setup.get_time()
            SGD.sgd(graph, width, height)
            torusSGD.torus_sgd(graph, width, height)
            drawGraph.create_compare_fig()

            _log = log.get_log()
            wh_log[str(time)] = _log

            message = str(time)
            print(message)

        all_log[str(_len)] = wh_log

    log.clear()
    time = setup.get_time()
    log.create_log(all_log)
