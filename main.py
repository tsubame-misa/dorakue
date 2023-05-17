import matplotlib.pyplot as plt
import networkx as nx
import json
import networkx as nx
from networkx.readwrite import json_graph
import random
import math
import plotly.express as px
from sklearn import preprocessing
from dorakue import dorakue_choice_center
from dorakue_bfs import dorakue_bfs
from kameKame import kamada_kawai


filename = './graph/les_miserables.json'
graph = json_graph.node_link_graph(json.load(open(filename)))

width = 800
height = 800

# 中心選ぶやつ
# res_choice_center = dorakue_choice_center(graph, width, height)
# print("choice")
# print(res_choice_center)
# print()

print("bfs")
res_bfs = dorakue_bfs(graph)
print(res_bfs)
print()

# print("kamada_kawai")
# res_kamada = kamada_kawai(graph, width, height)
# print(res_kamada)
