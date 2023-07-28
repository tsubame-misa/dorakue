import json
import pandas as pd
import glob
from common import calcDrawInfo, aestheticsMeasures
from networkx.readwrite import json_graph
import math
import re

tmp = {"edge_length_variance": 0,
       "minimum_angle": 0,
       "edge_crossings": 0,
       "dist_variance": 0,
       "dist_mean": 0,
       #    "wrap_dist_variance": 0,
       #    "wrap_dist_mean": 0,
       "delta_variance": 0,
       "delta_mean": 0,
       #    "wrap_delta_variance": 0,
       #    "wrap_delta_mean": 0,
       "count": 0}

torus_good_count = 0
all_graph_count = len(glob.glob("./result_sgd_0725_all_log/log/*"))

files = []
pd.set_option('display.max_columns', 20)
for filepath in glob.glob("./result_sgd_0725_all_log/log/*"):
    # json.load関数を使ったjsonファイルの読み込み
    # with open('./result_sgd_0725_2/log/cubical-20230724224257.json') as f:
    with open(filepath) as f:
        data = json.load(f)

    filename = re.split('[/-]', filepath)[-2]
    graph = json_graph.node_link_graph(
        json.load(open("./graph/"+filename+".json")))

    print(filepath, "node", len(graph.nodes), "edge", len(graph.edges))

    len_array = [_len for _len in data.keys()][1:]
    alg_array = ["SGD", "torusSGD"]

    result = dict()
    for _len in data.keys():
        alg_sum_result = {"SGD": tmp.copy(), "torusSGD": tmp.copy()}
        if _len == "file":
            continue
        for time in data[_len].keys():
            for alg in data[_len][time].keys():
                # 回り込みがなかった場合は集計しない
                if alg == "torusSGD":
                    if not data[_len][time][alg]["wrap"]:
                        print("no wrap")
                        continue

                if alg == "torusSGD":
                    pos = data[_len][time][alg]["pos"]
                    k = data[_len][time][alg]["k"]
                    l = data[_len][time][alg]["l"]
                    node_len = data[_len][time][alg]["node_len"]
                    d = data[_len][time][alg]["d"]
                    node2num = data[_len][time][alg]["node2num"]

                    # 回り込みあり
                    # delta = calcDrawInfo.calc_delta_around(
                    #     pos, k, l, node_len, float(_len), float(_len))
                    # alg_sum_result[alg]["wrap_dist_variance"] += data[_len][time][alg]["dist"]["sd"]
                    # alg_sum_result[alg]["wrap_dist_mean"] += data[_len][time][alg]["dist"]["mean"]
                    # alg_sum_result[alg]["wrap_delta_variance"] += aestheticsMeasures.calc_sd(
                    #     delta)
                    # alg_sum_result[alg]["wrap_delta_mean"] += aestheticsMeasures.calc_mean(
                    #     delta)

                    # まわりこみなし、torus描画を元に再計算
                    # delta = calcDrawInfo.calc_delta(pos, k, l, node_len)
                    # dist_score = [(d[node2num[str(u)]][node2num[str(v)]] -
                    #                calcDrawInfo.dist(pos, node2num[str(u)], node2num[str(v)]))**2 for u, v in graph.edges]

                    delta = calcDrawInfo.calc_delta_around(
                        pos, k, l, node_len, float(_len), float(_len))
                    dist_score = [(d[node2num[str(u)]][node2num[str(v)]] -
                                   calcDrawInfo.dist_around(pos, node2num[str(u)], node2num[str(v)], float(_len), float(_len), l[node2num[str(u)]][node2num[str(v)]]))**2 for u, v in graph.edges]
                    torus_evaluation = aestheticsMeasures.calc_torus_evaluation_values(
                        delta, dist_score, graph, node2num, pos, l, float(_len))

                    alg_sum_result[alg]["dist_mean"] += torus_evaluation["dist"]["mean"]
                    alg_sum_result[alg]["dist_variance"] += torus_evaluation["dist"]["sd"]
                    alg_sum_result[alg]["delta_variance"] += torus_evaluation["delta"]["sd"]
                    alg_sum_result[alg]["delta_mean"] += torus_evaluation["delta"]["mean"]

                    alg_sum_result[alg]["edge_length_variance"] += torus_evaluation["edge_length_variance"]
                    alg_sum_result[alg]["minimum_angle"] += torus_evaluation["minimum_angle"]
                    alg_sum_result[alg]["edge_crossings"] += torus_evaluation["edge_crossings"]
                    alg_sum_result[alg]["count"] += 1

                else:
                    alg_sum_result[alg]["dist_variance"] += data[_len][time][alg]["dist"]["sd"]
                    alg_sum_result[alg]["dist_mean"] += data[_len][time][alg]["dist"]["mean"]
                    alg_sum_result[alg]["delta_variance"] += data[_len][time][alg]["delta"]["sd"]
                    alg_sum_result[alg]["delta_mean"] += data[_len][time][alg]["delta"]["mean"]
                    # alg_sum_result[alg]["wrap_dist_variance"] += data[_len][time][alg]["dist"]["sd"]
                    # alg_sum_result[alg]["wrap_dist_mean"] += data[_len][time][alg]["dist"]["mean"]
                    # alg_sum_result[alg]["wrap_delta_variance"] += data[_len][time][alg]["delta"]["sd"]
                    # alg_sum_result[alg]["wrap_delta_mean"] += data[_len][time][alg]["delta"]["mean"]

                    alg_sum_result[alg]["edge_length_variance"] += data[_len][time][alg]["edge_length_variance"]
                    alg_sum_result[alg]["minimum_angle"] += data[_len][time][alg]["minimum_angle"]
                    alg_sum_result[alg]["edge_crossings"] += data[_len][time][alg]["edge_crossings"]
                    alg_sum_result[alg]["count"] += 1

        alg_mean_result = {}
        for alg in alg_sum_result.keys():
            alg_mean_result[alg] = {}
            count = alg_sum_result[alg]["count"]
            alg_mean_result[alg]["count"] = count
            if count == 0:
                continue
            for item in alg_sum_result[alg].keys():
                if item == "count":
                    continue
                alg_mean_result[alg][item] = alg_sum_result[alg][item]/count
        result[_len] = alg_mean_result

    diff = []
    goood_cnts = []
    _lens = []

    for i, _len in enumerate(result.keys()):
        _lens.append(_len)
        sgd_total = 0
        torus_sgd_total = 0
        t_good_cnt = 0
        for item in tmp:
            if item == "count":
                continue
            sgd_total += result[_len]["SGD"][item]
            torus_sgd_total += result[_len]["torusSGD"][item]
            # +torusの方が良い
            # -normlが良い
            if result[_len]["SGD"][item]-result[_len]["torusSGD"][item] >= 0:
                t_good_cnt += 1
        sgd_total /= result[_len]["SGD"]["count"]
        torus_sgd_total /= result[_len]["torusSGD"]["count"]
        # +torusの方が良い
        # -normlが良い
        diff.append(sgd_total-torus_sgd_total)
        goood_cnts.append(t_good_cnt)

    diff_count_max = goood_cnts.index(max(goood_cnts))
    best_len_index = [n for n, v in enumerate(diff) if v == diff_count_max]
    if best_len_index == 1:
        best_len = _lens[best_len_index[0]]
    else:
        best_len = _lens[diff.index(max(diff))]

    df = pd.DataFrame.from_dict(result[best_len])

    if max(goood_cnts) >= (len(tmp)-1)//2:
        torus_good_count += 1

    print("len", _lens)
    print("best len", best_len, "トーラスの方が良かった個数",
          max(goood_cnts), "diff", max(diff))
    pd.options.display.float_format = '{:.8f}'.format
    print(df.T)
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")

print("graph", all_graph_count, "torus_good_graph",
      torus_good_count, "%", torus_good_count/all_graph_count)
# print(result)
