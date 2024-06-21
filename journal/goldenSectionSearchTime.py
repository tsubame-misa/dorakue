import glob
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)+"/")

from networkx.readwrite import json_graph
import json
import re
import setup
from common import log
import time

from algorithm.SGDBase.egraphCellOptimazation import cell_optimazation

"""
黄金分割探索の実行時間を測る
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

    log_file_name = "test_time_gss_sparse"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        print(g["name"], len(g["graph"].nodes), len(g["graph"].edges),"-----------------")
        data = []
        for i in range(20):
            print(g["name"], i)
            _time = setup.get_time()
            index_time = str(i) + str(_time)   
            start = time.perf_counter() #計測開始    
            _log = cell_optimazation(g["graph"], g["name"], log_file_name, i, index_time)
            end = time.perf_counter() #計測終了
            _log["id"] = index_time
            _log["time"] = end-start
            data.append(_log)
        log.create_log(data, g["name"]+"-all")
        

if __name__ == '__main__':
    main()

import time