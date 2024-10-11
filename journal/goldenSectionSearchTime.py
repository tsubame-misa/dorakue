import argparse
import glob
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + "/")

from networkx.readwrite import json_graph
import json
import re
import setup
from common import log
import time

from algorithm.SGDBase.egraphCellOptimazation import cell_optimazation

"""
黄金分割探索の実行時間を測る
files = ./graphSet/networkx
files = ./graphSet/doughNetGraph/default
files = ./graphSet/randomPartitionNetwork 
files = ./graphSet/suiteSparse
"""


def main():
    parser = argparse.ArgumentParser()  # parserを定義

    # 受け取る引数を追加する
    parser.add_argument("log_file_name")
    parser.add_argument("--weighting", action="store_true")
    parser.add_argument("--loop", default=20)
    args = parser.parse_args()  # 引数を解析

    files = {
        "./graphSet0920/networkx/*",
        "./graphSet0920/doughNetGraph/default/*",
        "./graphSet0920/doughNetGraph0920/*",
        "./graphSet0920/randomPartitionNetwork/*",
        "./graphSet0920/randomPartitionNetwork0920/*",
        "./graphSet0920/suiteSparse/*",
        "./graphSet0920/suiteSparse0920/*",
    }
    golden_section_search(files, args.log_file_name, args.weighting, int(args.loop))


def golden_section_search(files, log_file_name, weigthing, loop):
    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split("[/]", filepath)[-1][:-5]
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))

    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    for g in sorted_graphs:
        if os.path.isfile(log_file_name + "/log/" + g["name"] + "-all-.json"):
            continue
        print(
            g["name"], len(g["graph"].nodes), len(g["graph"].edges), "-----------------"
        )
        data = []
        for i in range(loop):
            print(g["name"], i)
            _time = setup.get_time()
            index_time = str(i) + str(_time)
            start = time.perf_counter()  # 計測開始
            _log = cell_optimazation(
                g["graph"], g["name"], log_file_name, i, index_time, weigthing
            )
            end = time.perf_counter()  # 計測終了
            _log["id"] = index_time
            _log["time"] = end - start
            data.append(_log)
        log.create_log(data, g["name"] + "-all")


if __name__ == "__main__":
    main()

import time
