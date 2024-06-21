"""
drawing chen cell size layout
"""

import glob
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)+"/")

from networkx.readwrite import json_graph
import json
import re
import setup
from common import log

from algorithm.SGDBase.egraphTorusSGD import torus_sgd

"""
求められたセルサイズで再度トーラス描画を行う
"""

def main():
    files = glob.glob("./graphSet/networkx/*")
    files = glob.glob("./graphSet/doughNetGraph/default/*")
    files = glob.glob("./graphSet/randomPartitionNetwork /*")
    files = glob.glob("./graphSet/suiteSparse/*")

    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/]', filepath)[-1][:-5]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

    log_file_name = "test_chen_torus_cell_size_sparse"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        print(g["name"], len(g["graph"].nodes), "----------------------")
        data = []
        for i in range(20):
            print(g["name"],i)
            time = setup.get_time()
            index_time = str(i) + str(time)   
            _log = torus_sgd(g["graph"], g["name"], log_file_name, random_idx=i, time=index_time, is_chen=True)
            _log["id"] = index_time
            data.append(_log)
        log.create_log(data, g["name"]+"-all")
        

if __name__ == '__main__':
    main()