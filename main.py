import json
from networkx.readwrite import json_graph
from algorithm.SGDBase import SGD, torusSGD, sparseSGD
from algorithm.kamadaKawaiBase import kameKame, torusKameCenter
import setup
from common import log, drawGraph, calcDrawInfo, aestheticsMeasures, debug, initGraph
from algorithm import torusCenter, torusBfs
import re


file_path = './graph/qh882.json'
# file_path = "./contest_graph/small.json"
# file_path = "./graph/qh882.json"
graph = json_graph.node_link_graph(json.load(open(file_path)))

file_name = re.split('[/.]', file_path)[3]
width = 3100
height = 3100

setup.init()
maxd = initGraph.get_maxd(graph, file_name)
print(maxd)


# print("torus_kame")
# torusKameCenter.torus_kame(graph, file_name, width, height)
# print()

# print("kamada_kawai")
# kameKame.kamada_kawai(graph, file_name, width, height)
# print()

print("SGD")
SGD.sgd(graph, file_name, width, height)
print("torusSGD")
torusSGD.torus_sgd(graph, file_name, width, height)
# setup.init()
# sparseSGD.sparse_sgd(graph, width, height)

# calcDrawInfo.compare_node_pos()

time = setup.get_time()
log.add_log("width", width)
log.add_log("height", height)
log.create_log()
drawGraph.create_compare_fig(file_name)
