
import glob
from networkx.readwrite import json_graph
import json
from algorithm.SGDBase.torusGoldenSearchSGD import torus_golden_search
import setup
from common import log, initGraph
import re
import matplotlib.pyplot as plt

def main():
    files = glob.glob("./graphSet/networkx/*")

    with open("./graphSet/info2.json") as f:
        graph_info = json.load(f)

    # 使用するグラフをノード数順に並び替える
    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/.]', filepath)[4]
        # typeA, Dは省く
        if graph_info["Networkx"][file_name]["type"] == "a" or graph_info["Networkx"][file_name]["type"] == "d":
            continue
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    
    log_file_name = "test_comp"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()


    for g in sorted_graphs:
        # if g["name"] != "frucht":
        #     continue
        print(g["name"], "size", len(g["graph"].nodes))
        all_log = []
        cnt = 10
        for i in range(cnt):
            initGraph.clear()
            print("#loop",i, g["name"])
            nomal = torus_golden_search(g["graph"], g["name"], log_file_name, 20)
            # pre = torus_golden_search(g["graph"], g["name"], log_file_name, use_pre_pos=1, True, i)
            scaled = torus_golden_search(g["graph"], g["name"], log_file_name, use_pre_pos=2, debug=True, index=i)
            _log = {
                "avg1":nomal,
                # "pre":pre,
                "scaled":scaled
            }
            all_log.append(_log)
        
        log.create_log(all_log, g["name"]+"-all")


if __name__ == '__main__':
    main()