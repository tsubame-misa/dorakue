import glob
import json
import matplotlib.pyplot as plt
import seaborn as sns
import re
import pandas as pd


def get_decreas_stop_size(data, optimal_cell_size):
    pre_stress = -1
    cnt = 0
    for key in data.keys():
        value = data[key]
        stress = sorted([d["multiple_num"] for d in value])
        stress_median = stress[len(value) // 2]
        if pre_stress != -1:
            if (
                pre_stress / stress_median >= 0.95
                and pre_stress / stress_median <= 1.05
            ):
                cnt += 1
        pre_stress = stress_median
        if cnt == 3:
            return float(key)
    return optimal_cell_size


def list2dict(data):
    data_dict = {}
    for d in data:
        data_dict.update(d)
    return data_dict


def main():
    # log_files = [
    #     "./graphDrawing/data/egraph/liner_egraph_networkx_20/log/save_best_len_log/*",
    #     "./graphDrawing/data/egraph/liner_egraph_dough_20/log/save_best_len_log/*",
    #     "./graphDrawing/data/egraph/liner_egraph_random_20/log/save_best_len_log/*",
    #     "./graphDrawing/data/egraph/liner_egraph_sparse_20/log/save_best_len_log/*",
    # ]
    # rename = False

    log_files = [
        "./journal/data/weigthing_liner/networkx/log/*",
        "./journal/data/weigthing_liner/dough0920/log/*",
        "./journal/data/weigthing_liner/douh/log/*",
        "./journal/data/weigthing_liner/random0920/log/*",
        "./journal/data/weigthing_liner/random/log/*",
        "./journal/data/weigthing_liner/sparse/log/*",
        "./journal/data/weigthing_liner/sparse0929/log/*",
        "./journal/data/weigthing_liner/sparse1014/log/*",
    ]
    rename = True

    with open("./graphSet0920/info_weigthed.json") as f:
        _graph_info = [g for g in json.load(f).values()]

    with open("./graphSet0920/chen_weighting_cell_size_median.json") as f:
        chen_cell_size = json.load(f)

    graph_info = list2dict(_graph_info)
    for key in graph_info.keys():
        graph_info[key]["append"] = False

    cell_size = {"TORUS": [], "NO-TORUS": []}
    for files_name in log_files:
        files = glob.glob(files_name)
        for file in files:
            file_name = re.split("[/]", file)[-1][:-6]
            if not file_name in graph_info or graph_info[file_name]["append"]:
                continue
            with open(file) as f:
                data = json.load(f)
            if rename:
                diff = chen_cell_size[file_name] - data["optimal_cell_size"]
            else:
                diff = chen_cell_size[file_name] - data["best_multiple_num"]

            if graph_info[file_name]["type"] == "a":
                cell_size["NO-TORUS"].append(diff)
            else:
                cell_size["TORUS"].append(diff)
            graph_info[file_name]["append"] = True

    print(cell_size)

    # データフレームに変換
    df = pd.DataFrame(
        [(v, k) for k, values in cell_size.items() for v in values],
        columns=["Value", "Type"],
    )

    # プロットの作成
    plt.figure(figsize=(8, 6))
    sns.boxplot(
        x="Value", y="Type", data=df, order=["TORUS", "NO-TORUS"], color="white"
    )
    plt.title("Boxplot of TORUS and NO-TORUS Types")
    plt.show()


if __name__ == "__main__":
    main()
