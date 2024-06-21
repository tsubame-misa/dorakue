import glob
import json
import re
from scipy.io import loadmat
import networkx as nx
import sys

args = sys.argv

files = glob.glob("./" + args[1] + "/*")

for path in files:
    print(path)
    try:
        mat = loadmat(path)
    except NotImplementedError:
        print("error", path)

    name = re.split("[/]", path)[-1][:-4]
    print(name)

    problem = mat["Problem"].tolist()
    sparse_matrix = problem[0][0][1]

    # Create a graph from the sparse matrix
    graph = nx.from_scipy_sparse_array(sparse_matrix)

    data = nx.node_link_data(graph)

    n_data = dict()
    for k in data.keys():
        if k == "graph":
            n_data["graph"] = {"name": name}
        if k in ["directed", "multigraph", "nodes"]:
            n_data[k] = data[k]
        if k == "links":
            n_data["links"] = []
            for _link in data["links"]:
                if _link["source"] != _link["target"]:
                    n_data["links"].append(_link)

        # if k == "nodes":
        #     n_data["nodes"] = []
        #     for _node in data["nodes"]:
        #         n_data["nodes"].append({"id": _node["id"]})

    with open("./matDataJson/" + name + ".json", "w") as f:
        json.dump(n_data, f)
