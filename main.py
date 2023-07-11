import json
from networkx.readwrite import json_graph
from algorithm.SGDBase import SGD, torusSGD, sparseSGD, test
from algorithm.kamadaKawaiBase import kameKame, torusKameCenter
import setup
from common import log, drawGraph, calcDrawInfo
from algorithm import torusCenter, torusBfs


filename = './graph/les_miserables.json'
# filename = "./contest_graph/small.json"
# filename = "./graph/USpowerGrid.json"
graph = json_graph.node_link_graph(json.load(open(filename)))

width = 200000
height = 200000

setup.init()
# setup.set_roop1(200)
# 中心選ぶやつ
# print("choice")
# torusCenter.torus_center(graph, width, height)
# print()

# print("bfs")
# torusBfs.torus_bfs(graph, width, height)
# print()

# setup.set_roop1(50)
# print("torus_kame")
# torusKameCenter.torus_kame(graph, width, height)
# print()

# print("kamada_kawai")
# kameKame.kamada_kawai(graph, width, height)
# print()
# SGD.sgd(graph, width, height)
# torusSGD.torus_sgd(graph, width, height)
# setup.init()
sparseSGD.sparse_sgd(graph, width, height)
# test.sparse_sgd(graph, width, height)

# calcDrawInfo.compare_node_pos()

time = setup.get_time()
log.add_log("width", width)
log.add_log("height", height)
log.create_log()
drawGraph.create_compare_fig()
