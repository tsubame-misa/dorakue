import json
from networkx.readwrite import json_graph
from dorakue import dorakue_choice_center
from dorakue_bfs import dorakue_bfs
from kameKame import kamada_kawai
import common
import commonLog
import commonDrawGraph


filename = './graph/les_miserables.json'
graph = json_graph.node_link_graph(json.load(open(filename)))

width = 1000
height = 1000

common.init()

# 中心選ぶやつ
print("choice")
dorakue_choice_center(graph, width, height)
print()

print("bfs")
dorakue_bfs(graph, width, height)
print()

print("kamada_kawai")
kamada_kawai(graph, width, height)
print()

time = common.get_time()
commonLog.add_log("width", width)
commonLog.add_log("height", height)
commonLog.create_log()
commonDrawGraph.create_compare_fig()
