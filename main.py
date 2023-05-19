import json
from networkx.readwrite import json_graph
from dorakue import dorakue_choice_center
from dorakue_bfs import dorakue_bfs
from kameKame import kamada_kawai
import common


filename = './graph/les_miserables.json'
graph = json_graph.node_link_graph(json.load(open(filename)))

width = 1000
height = 1000

common.clear()

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
common.add_log("width", width)
common.add_log("height", height)
common.create_log(time)
common.create_compare_fig(time)
