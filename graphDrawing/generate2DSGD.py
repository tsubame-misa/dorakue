import glob
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)+"/")

from networkx.readwrite import json_graph
import json
from algorithm.SGDBase.egraphSGD import sgd
import setup
from common import log, initGraph
import re

def main():
    files = glob.glob("./graphSet/networkx/*")
    files = glob.glob("./graphSet/sample/*")
    # files = glob.glob("./graphSet/doughNetGraph/default/*")
    # files = glob.glob("./graphSet/randomPartitionNetwork /*")

    # 使用するグラフをノード数順に並び替える
    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/]', filepath)[-1][:-5]
        print(file_name)
        obj = {"name": file_name, "graph": graph}
        graphs.append(obj)
    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    
    log_file_name = "test_9"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()


    for g in sorted_graphs:
        print(g["name"], "size", len(g["graph"].nodes))
        all_log = []
        cnt = 20
        for i in range(cnt):
            initGraph.clear()
            if not(g["name"]=="9-4" or g["name"]=="9-4-2"):
                continue
            print("#loop",i, g["name"])
            time = setup.get_time()
            index_time = str(i) + str(time)
            _log = sgd(g["graph"], g["name"], log_file_name, i, time=index_time)
            all_log.append(_log)
        
        log.create_log(all_log, g["name"]+"-all")


if __name__ == '__main__':
    main()