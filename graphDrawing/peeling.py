
import glob
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)+"/")
from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt
import networkx as nx
from common import log
import setup
from  generateColorGraph import get_chromatic_number

import csv
import statistics


"""
ピーリングをして、グラフの次数の平均、分散を計算
"""

def peeling_graph(G, name, dir_name):
    node_be=G.number_of_nodes() #削除前の頂点数
    edge_be=G.number_of_edges() #削除前の辺数
    #[次数が0の頂点]もしくは[次数が1の頂点とその頂点に接続する辺]を削除する
    G_rem=[]
    #条件に合う頂点をリストアップする
    for i in range(node_be):
        for v in G:
            G_deg=G.degree(v)
            if G_deg<=1:
                G_rem.append(v)
        #条件に合う頂点を削除する
        G.remove_nodes_from(G_rem)

    node_af=G.number_of_nodes() #削除後の頂点数
    edge_af=G.number_of_edges() #削除後の辺数

    if node_be!=node_af:
        print("nodes", node_be, node_af)
        print("edge", edge_be, edge_af)

    new_dir_path = './' + dir_name + "/SGD/" 
    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    #グラフの出力
    # nx.draw_networkx(G)
    # img_path = './' + dir_name+'/SGD/' + name+'.png'
    # plt.savefig(img_path)
    # plt.clf()
    # plt.close()

    return G


def calc_graph_degree(G):
    # node_be=G.number_of_nodes() #削除前の頂点数
    # edge_be=G.number_of_edges() #削除前の辺数
    # print(node_be)
    degrees =  [G.degree(v) for v in G.nodes]
    avg = statistics.median(degrees)
    s2 = statistics.pvariance(degrees) #sum([(d-avg)**2 for d in degrees])/len(degrees)
    mid = statistics.median(degrees)
    mod = statistics.mode(degrees)
    q1, q2, q3 = statistics.quantiles(degrees, n=4)
    quartile_deviation = (q3-q1)/2

    print(avg, s2)

    return {"avg":avg, "s2":s2, "midian":mid, "mod":mod, "quartile_deviation":quartile_deviation}


def main():
    files = glob.glob("./graphSet/networkx/*")
    # files = glob.glob("./graphSet/doughNetGraph/default/*")
    # files = glob.glob("./graphSet/randomPartitionNetwork /*")
    # files = glob.glob("./graphSet/suiteSparse/*")


    with open("./graphSet/info2.json") as f:
        graph_info = json.load(f)

    graphs = []
    for filepath in files:
        graph = json_graph.node_link_graph(json.load(open(filepath)))
        file_name = re.split('[/]', filepath)[-1][:-5]
        obj = {"name": file_name, "graph": graph, "type":graph_info["Networkx"][file_name]["type"]}
        # obj = {"name": file_name, "graph": graph, "type":graph_info["Real world"][file_name]["type"]}
        # obj = {"name": file_name, "graph": graph, "type":graph_info["Random Partition2"][file_name]["type"]}
        # obj = {"name": file_name, "graph": graph, "type":graph_info["SuiteSparse Matrix"][file_name]["type"]}
        graphs.append(obj)


    sorted_graphs = sorted(graphs, key=lambda x: len(x["graph"].nodes))
    log_file_name = "peeling_test"
    setup.set_dir_name(log_file_name)
    log.create_log_folder()

    csv_data = [["name", "type", "chromatic_num", "degree_avg", "degree_s2","degree_midian", "degree_mod", "degree_quartile_deviation" "node", "peeled nodes", "edges", "peeled edges"]]

    for g in sorted_graphs:
        # if g["name"]=="lowThrust_1":
        #     continue
        node_be = g["graph"].number_of_nodes()
        edge_be = g["graph"].number_of_edges()
        print(g["name"], "size", len(g["graph"].nodes))
        peeled_graph = peeling_graph(g["graph"], g["name"], log_file_name)
        degree_result = calc_graph_degree(peeled_graph)
        chromatic_num = get_chromatic_number(g["graph"], g["name"])
        csv_data.append([g["name"], g["type"], chromatic_num,  degree_result["avg"], degree_result["s2"], degree_result["midian"], degree_result["mod"], degree_result["quartile_deviation"],
                         node_be, peeled_graph.number_of_nodes(), edge_be, peeled_graph.number_of_edges()])
        print("---------------------")

    # CSVファイル名
    csv_file = "degree_info_network" + ".csv"
    # CSVファイルにデータを書き込む
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # データ行を書き込む
        writer.writerows(csv_data)


if __name__ == '__main__':
    main()
