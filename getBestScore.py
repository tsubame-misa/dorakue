import json
import glob
import re
import os
from common import drawGraph, log, calcDrawInfo,  initGraph, aestheticsMeasures, debug
from networkx.readwrite import json_graph
import setup

"""
ログフォルダにある複数のログから、一番いいもののscoreだけそbest_scoreに
※ 一番いいものって数値的にどうするのがいいんだ

TODO:allSGDに組み込みたい？
"""

folder_name = "result_douhnet_1012"
for filepath in glob.glob("./" + folder_name + "/log/*"):
    with open(filepath) as f:
        data = json.load(f)
    len_array = [_len for _len in data.keys()][1:]
    score = []
    for time in data[len_array[0]]:
        s = {"edge_length_variance": data[len_array[0]][time]["torusSGD"]["edge_length_variance"],
             "minimum_angle": data[len_array[0]][time]["torusSGD"]["minimum_angle"],
             "edge_crossings": data[len_array[0]][time]["torusSGD"]["edge_crossings"],
             "delta": data[len_array[0]][time]["torusSGD"]["delta"],
             "dist": data[len_array[0]][time]["torusSGD"]["dist"],
             "time": time}
        score.append(s)

    sorted_score = sorted(
        score,  key=lambda x: (x["minimum_angle"] * x["edge_crossings"]))

    path = os.getcwd()
    new_dir_path = path + "/" + folder_name+"/best_score"

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    with open(path + "/" + folder_name + "/best_score/" + data["file"] + ".json", "w") as f:
        json.dump(sorted_score[0], f)
