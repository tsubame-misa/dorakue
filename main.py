import json
from networkx.readwrite import json_graph
import setup
from common import log, drawGraph
from algorithm import torusCenter, torusBfs, kameKame


filename = './graph/les_miserables.json'
graph = json_graph.node_link_graph(json.load(open(filename)))

width = 1000
height = 1000

setup.init()
setup.set_roop1(3)

# 中心選ぶやつ
print("choice")
torusCenter.torus_center(graph, width, height)
print()

print("bfs")
torusBfs.torus_bfs(graph, width, height)
print()

print("kamada_kawai")
kameKame.kamada_kawai(graph, width, height)
print()

time = setup.get_time()
log.add_log("width", width)
log.add_log("height", height)
log.create_log()
drawGraph.create_compare_fig()
