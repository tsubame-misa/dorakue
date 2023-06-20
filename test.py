
import glob
from networkx.readwrite import json_graph
import json
from multiMainSGD import create_sgd_graph
from multiMainKK import create_kk_graph
import setup
from common import log, drawGraph, calcDrawInfo
from collections import defaultdict
import os

files = glob.glob("./all_result/result_under800nodes/log/*")
graphs = []
len_list = setup.get_len()


for filepath in files:
    with open(filepath) as f:
        data = json.load(f)
        print(data["file"], filepath)
        sgd_flg = False
        for _len in len_list:
            img_dict = dict()
            delta_count = 0
            dist_count = 0
            delta_diff = dict()
            dist_diff = dict()
            for time, time_v in data[str(_len)].items():
                for alg, alg_v in time_v.items():
                    img_path = "./all_result/result_under800nodes/" + \
                        alg + "/" + str(_len) + "x" + \
                        str(_len) + "-" + time+".png"

                    if alg in img_dict:
                        img_dict[alg].append(img_path)
                    else:
                        img_dict[alg] = [img_path]

                    if alg == "SGD":
                        sgd_flg = True

                if sgd_flg:
                    if time_v["SGD"]["delta"]["sd"] >= time_v["torusSGD"]["delta"]["sd"]:
                        delta_count += 1
                        # プラスだとtorusが小さいので嬉しい
                    if time_v["SGD"]["dist"]["sd"] >= time_v["torusSGD"]["dist"]["sd"]:
                        dist_count += 1
                    delta_diff[time] = time_v["SGD"]["delta"]["sd"] - \
                        time_v["torusSGD"]["delta"]["sd"]
                    dist_diff[time] = time_v["SGD"]["dist"]["sd"] - \
                        time_v["torusSGD"]["dist"]["sd"]
                else:
                    if time_v["kamada_kawai"]["delta"]["sd"] >= time_v["torus_kame"]["delta"]["sd"]:
                        delta_count += 1
                    if time_v["kamada_kawai"]["dist"]["sd"] >= time_v["torus_kame"]["dist"]["sd"]:
                        dist_count += 1
                    delta_diff[time] = time_v["kamada_kawai"]["delta"]["sd"] - \
                        time_v["torus_kame"]["delta"]["sd"]
                    dist_diff[time] = time_v["kamada_kawai"]["dist"]["sd"] - \
                        time_v["torus_kame"]["dist"]["sd"]

            # サイズ、手法ごとにグラフ描画をまとめたpngを作成
            for alg, img_path in img_dict.items():
                log_name = data["file"].split(".")[0]+str(_len)+alg
                drawGraph.get_single_alg_figs(
                    log_name, img_path)

            # サイズ、手法での比較結果のログを作成
            _log = {
                "dist": dist_count/10,
                "delta": delta_count/10,
                "dist_diff": dist_diff,
                "delta_diff": delta_diff,

            }
            path = os.getcwd()
            log_name = data["file"].split(".")[0]+str(_len)
            log_name += "SGD" if sgd_flg else "kamada-kawai"
            with open(path + "/comp_result/single/log/" + log_name + ".json", "w") as f:
                json.dump(_log, f)
