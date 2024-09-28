import argparse
import networkx as nx
import matplotlib.pyplot as plt
import json


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("node", type=int)
    parser.add_argument("file_name")
    parser.add_argument("kind")
    parser.add_argument("--node2", default=0, type=int)
    args = parser.parse_args()
    print(args)

    generateGraph(args.node, args.file_name, args.kind, args.node2)


def generateGraph(node, name, kind, node2):

    if kind == "0":
        G = nx.scale_free_graph(
            node,
            alpha=0.025,
            beta=0.95,
            gamma=0.025,
            delta_in=2.0,
            delta_out=2.0,
        )
        # G = nx.scale_free_graph(
        #     node,
        # )
    elif kind == "1":
        print("small")
        G = nx.watts_strogatz_graph(node, 5, 0.35)
    elif kind == "2":
        G = nx.complete_graph(node, create_using=None)
    elif kind == "3":
        G = nx.complete_bipartite_graph(node, node2)
    elif kind == "4":
        G = nx.random_partition_graph([node] * 10, p_in=0.9, p_out=0.02)

    undirected_G = G.to_undirected()
    largest_cc = max(nx.connected_components(undirected_G), key=len)
    largest_sub_graph = undirected_G.subgraph(largest_cc).copy()
    scale_free_graph = nx.Graph(largest_sub_graph)
    for j in scale_free_graph.nodes:
        if scale_free_graph.has_edge(j, j):
            scale_free_graph.remove_edge(j, j)
    data = nx.node_link_data(scale_free_graph)

    nx.draw_networkx(scale_free_graph, node_size=5, with_labels=None, width=0.5)
    plt.show()
    print("show", len(scale_free_graph.edges))

    n_data = dict()
    for k in data.keys():
        if k == "graph":
            n_data["graph"] = {"name": name}
        if k in ["directed", "multigraph", "links"]:
            n_data[k] = data[k]
        if k == "nodes":
            n_data["nodes"] = []
            for _node in data["nodes"]:
                n_data["nodes"].append({"id": _node["id"]})

    with open(name + ".json", "w") as f:
        json.dump(n_data, f)


if __name__ == "__main__":
    main()
