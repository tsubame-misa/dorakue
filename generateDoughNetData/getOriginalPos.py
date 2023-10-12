import json
import glob
import re
import os

for filepath in glob.glob("./doughNetGraph/origin/*"):
    with open(filepath) as f:
        data = json.load(f)["graph"]
        filename = re.split('[/.-]', filepath)[-2]
        path = os.getcwd()

        nodes = []

        for node in data["nodes"]:
            new_node = {
                "id": node["nodeIndex"]
            }
            nodes.append(new_node)

        pos = [None]*len(nodes)

        for link in data["links"]:
            if pos[link["source"]["nodeIndex"]] is None:
                pos[link["source"]["nodeIndex"]] = [
                    link["source"]["x"], link["source"]["y"]]

            if pos[link["target"]["nodeIndex"]] is None:
                pos[link["target"]["nodeIndex"]] = [
                    link["target"]["x"], link["target"]["y"]]

         # 新しいJSONデータを生成
        new_data = {
            "nodes": nodes,
            "pos": pos,
            "file": filename,
        }

        path = os.getcwd()

        with open(path + "/doughNetGraph/pos_only/" + filename+".json", "w") as f:
            json.dump(new_data, f)
