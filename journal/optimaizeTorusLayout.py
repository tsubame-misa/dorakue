"""
drawing optimaize cell size layout
"""

import glob
import os
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent) + "/")

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
    # files = glob.glob("./graphSet/doughNetGraph/default/*")
    # files = glob.glob("./graphSet/randomPartitionNetwork /*")
    # files = glob.glob("./graphSet/suiteSparse/*")
    cell_size_files = glob.glob(
        "./graphDrawing/data/egraph/liner_egraph_networkx_20/log/save_best_len_log/*"
    )
    # cell_size_files = glob.glob(
    #     "./graphDrawing/data/egraph/liner_egraph_dough_20/log/save_best_len_log/*"
    # )
    # cell_size_files = glob.glob(
    #     "./graphDrawing/data/egraph/liner_egraph_random_20/log/save_best_len_log/*"
    # )

    cell_info = dict()

    for filepath in cell_size_files:
        with open(filepath) as f:
            data = json.load(f)
        file_name = re.split("[/]", filepath)[-1][:-6]
        cell_info[file_name] = data["best_multiple_num"]

    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split("[/]", filepath)[-1][:-5]
        obj = {"name": file_name, "graph": graph, "optimalCellSize": cell_size_files}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

    log_file_name = "test"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        print(g["name"], "------------------------------")
        # if os.path.isfile(log_file_name + "/log/" + g["name"] + "-all-.json"):
        #     continue
        data = []
        for i in range(5):
            if g["name"] != "les_miserables":
                continue

            print(g["name"], i)
            _time = setup.get_time()
            index_time = str(i) + str(_time)
            start = time.perf_counter()  # 計測開始
            _log = torus_sgd(
                g["graph"],
                g["name"],
                log_file_name,
                # cell_info[g["name"]],
                4,
                i,
                index_time,
            )
            end = time.perf_counter()  # 計測終了
            _log["id"] = index_time
            _log["time"] = end - start
            data.append(_log)
        log.create_log(data, g["name"] + "-all")


if __name__ == "__main__":
    main()
