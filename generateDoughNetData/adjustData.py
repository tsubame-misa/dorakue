import json
import glob
import re
import os

for filepath in glob.glob("./doughNetGraph/origin/*"):
    with open(filepath) as f:
        data = json.load(f)["graph"]
        filename = re.split('[/.-]', filepath)[-2]
        path = os.getcwd()

        # 新しいJSONデータを生成
        new_data = {
            "links": [],
            "nodes": [],
            "directed": False,
            "multigraph": False,
            "graph": {"name": filename},
        }

        for link in data["links"]:
            new_link = {
                "source": link["source"]["nodeIndex"],
                "target": link["target"]["nodeIndex"],
            }
            new_data["links"].append(new_link)

        for node in data["nodes"]:
            new_node = {
                "id": node["nodeIndex"]
            }
            new_data["nodes"].append(new_node)

        path = os.getcwd()

        with open(path + "/doughNetGraph/default/" + filename+".json", "w") as f:
            json.dump(new_data, f)
