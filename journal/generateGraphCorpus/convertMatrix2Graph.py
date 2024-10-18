import matplotlib.pyplot as plt
import scipy.io as scio
import os
import networkx as nx
import json
import argparse
import glob


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("log_folder")
    args = parser.parse_args()
    generateGraph(args.folder, args.log_folder)


def generateGraph(folder, log_folder):
    files = glob.glob(folder + "/*")

    for path in files:
        m = scio.mmread(path)
        # 正方行列だけ扱う
        if m.shape[0] != m.shape[1]:
            continue
        name, ext = os.path.splitext(os.path.basename(path))

        G = nx.Graph()
        edges = []

        G.add_nodes_from([i for i in range(m.shape[0])])

        # 非ゼロの要素を参照
        rows, cols = m.nonzero()
        for r, c in zip(rows, cols):
            if r != c:
                edges.append((r.item(), c.item()))

        G.add_edges_from(edges)

        nx.draw(
            G,
            with_labels=False,
        )
        plt.show()

        n_data = {
            "graph": {"name": name},
            "directed": False,
            "multigraph": False,
            "links": [{"source": u, "target": v} for u, v in edges],
            "nodes": [{"id": i} for i in range(m.shape[0])],
        }

        with open(log_folder + "/" + name + ".json", "w") as f:
            json.dump(n_data, f)


if __name__ == "__main__":
    main()
