import glob
from networkx.readwrite import json_graph
import json
from multiMainSGD import create_sgd_graph
from multiMainKK import create_kk_graph
import setup

files = glob.glob("./graph/*")
graphs = []

for filepath in files:
    graph = json_graph.node_link_graph(json.load(open(filepath)))
    filename = filepath.split("/")[-1]
    obj = {"name": filename, "graph": graph}
    graphs.append(obj)


sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

for g in sorted_graphs:
    if len(g["graph"].nodes) < 800:
        continue
    print(g["name"], "size", len(g["graph"].nodes))
    setup.set_term(10)
    create_sgd_graph(g["graph"], g["name"])
    create_kk_graph(g["graph"], g["name"])
    print("---------------------")
