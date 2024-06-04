
import glob
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)+"/")

from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt
import setup
from common import log

from algorithm.SGDBase.egraphTorusSGD import torus_sgd

"""
求められたセルサイズで再度トーラス描画を行う
"""
def main():
    files = glob.glob("./graphSet/networkx/*")

    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/]', filepath)[-1][:-5]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

    log_file_name = "test"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        # if g["name"] != "house_x":
        #     continue
        log_file_candidate = glob.glob("./graphDrawing/data/my_algorithm/networkx_0508_20/"+"/log/"+g["name"]+'-all*')
        if len(log_file_candidate)==0:
            continue
        print(g["name"])
        with open(log_file_candidate[0]) as f:
            data = json.load(f)
            all_log = []
            for i in range(len(data)):  
                time = setup.get_time()
                index_time = str(i) + str(time)          
                _log = torus_sgd(g["graph"], g["name"], "test", data[i]["multipl_number"], time=index_time)
                all_log.append(_log)
    
        log.create_log(all_log, g["name"]+"-all")

    

if __name__ == '__main__':
    main()