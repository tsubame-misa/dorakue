import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import SGD, torusSGD
from common import drawGraph, log, initGraph
import re


def create_graph(graph, file_name):
    maxd = initGraph.get_maxd(graph, file_name)
    # len_list = [maxd*0.25, maxd*0.5, maxd * 0.75,  maxd, maxd *
    #             (2**0.5), maxd*2, maxd*3, maxd*4, maxd*5, maxd*6, maxd*7, maxd*8, maxd*9]
    len_list = [maxd*0.2, maxd*0.4,  maxd*0.6, maxd*0.8, maxd, maxd*1.2, maxd*1.4, maxd*1.6,maxd*1.8,maxd*2]
    # len_list = [maxd]
    # len_list = [maxd*0.75]

    all_log = {"file": file_name}
    for _len in len_list:
        width = _len
        height = _len
        wh_log = {}

        if len(g["graph"].nodes) >= 0:
            setup.set_term(1)

        term = setup.get_term()
        for i in range(term):
            setup.init()
            setup.set_dir_name(log_file_name)
            time = setup.get_time()
            index_time = str(i) + str(time)
            drawGraph.set_time(index_time)
            SGD.sgd(graph, file_name, width, height)
            torusSGD.torus_sgd(graph, file_name, width, height)
            drawGraph.create_compare_fig(file_name)
            _log = log.get_log()
            wh_log[str(index_time)] = _log

            message = str(index_time)
            print(message)

        all_log[str(_len)] = wh_log

    log.clear()
    time = setup.get_time()
    log.create_log(all_log, file_name)


# files = glob.glob("./doughNetGraph/default/*")
files = glob.glob("./graph/*")
graphs = []

for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    # file_name = filepath.split("/")[-1]
    file_name = re.split('[/.]', filepath)[3]
    # file_name = re.split('[/.]', filepath)[-2]
    obj = {"name": file_name, "graph": graph}
    graphs.append(obj)


sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
log_file_name = "result_1117_detail"
setup.set_dir_name(log_file_name)
log.create_log_folder()

graph_names = ["hoffman_singleton", "chvatal", "icosahedral",
               "dodecahedral", "florentine_families", "moebius_kantor"]
# graph_names = ["hoffman_singleton",
#                "dodecahedral", "florentine_families", "moebius_kantor"]


for g in sorted_graphs:
    # if len(g["graph"].nodes) < 100:
    #     continue
    if not g["name"] in graph_names:
        continue
    # if g["name"] != "hoffman_singleton":
    #     continue
    print(g["name"], "size", len(g["graph"].nodes))
    create_graph(g["graph"], g["name"])
    print("---------------------")
