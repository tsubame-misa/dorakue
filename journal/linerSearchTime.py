"""
線形探索の時間を測る

一回分の平均実行時間 × 試行回数で概算する
"""

import argparse
import glob
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).parent.parent) + "/")

import glob
from networkx.readwrite import json_graph
import json
import setup
from algorithm.SGDBase import egraphTorusSGD
from common import log
import re
import os


def get_time_avg(data):
    times = [d["time"] for d in data]
    return sum(times) / len(times)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file_name")
    parser.add_argument("--weighting", action="store_true")
    parser.add_argument("--loop", default=20)
    args = parser.parse_args()
    log_file_name = args.log_file_name
    loop = int(args.loop)

    with open("./graphSet0920/chen_weighting_cell_size_median.json") as f:
        chen_cell_size_info = json.load(f)

    graphs = []
    for f in glob.glob("./graphSet0920/*"):
        files = glob.glob(f + "/*")
        for f in files:
            file_name = re.split("[/]", f)[-1][:-5]
            graph = json_graph.node_link_graph(json.load(open(f)))
            obj = {"name": file_name, "graph": graph}
            graphs.append(obj)

    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes), reverse=True)

    for g in sorted_graphs:
        if os.path.isfile(log_file_name + "/log/" + g["name"] + "-all-.json"):
            continue
        print(
            g["name"], len(g["graph"].nodes), len(g["graph"].edges), "-----------------"
        )

        setup.set_dir_name(log_file_name)
        log.create_log_folder()

        data = []

        for i in range(loop):
            print(g["name"], i)
            _time = setup.get_time()
            index_time = str(i) + str(_time)
            start = time.perf_counter()  # 計測開始
            _log = egraphTorusSGD.torus_sgd(
                g["graph"],
                g["name"],
                log_file_name,
                chen_cell_size_info[g["name"]],
                weigthing=True,
            )
            end = time.perf_counter()  # 計測終了
            _log["id"] = index_time
            _log["time"] = end - start
            data.append(_log)
        log.create_log(data, g["name"] + "-all")


if __name__ == "__main__":
    main()
