import json
import pandas as pd
import glob
from common import calcDrawInfo, aestheticsMeasures
from networkx.readwrite import json_graph
import math
import re
import torusGraphDrawing
import setup
from common import drawGraph

all_graph_count = len(glob.glob("./result_sgd_0725_all_log/log/*"))

log_file_name = "result_sgd_0725_all_log"
setup.set_dir_name(log_file_name)

for filepath in glob.glob("./result_sgd_0725_all_log/log/*"):
    with open(filepath) as f:
        data = json.load(f)

    filename = re.split('[/-]', filepath)[-2]
    graph = json_graph.node_link_graph(
        json.load(open("./graph/"+filename+".json")))

    print(filepath, "node", len(graph.nodes), "edge", len(graph.edges))

    len_array = [_len for _len in data.keys()][1:]
    alg_array = ["SGD", "torusSGD"]

    result = dict()
    for _len in data.keys():
        if _len == "file":
            continue
        for time in data[_len].keys():
            for alg in data[_len][time].keys():
                if alg == "torusSGD":
                    dir_name = setup.get_dir_name()
                    img_path = drawGraph.get_dir()+'/'+dir_name+'/torusSGDTrue/' + filename + \
                        "-" + _len + "-" + time + '.png'
                    torusGraphDrawing.graph_drawing(
                        data[_len][time][alg], graph,  float(_len), img_path, True)
