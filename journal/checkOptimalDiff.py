import glob
import re
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def list2dict(data):
    data_dict = {}
    for d in data:
        data_dict.update(d)
    return data_dict


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


def get_score(data, _type, optimal_cell_size):
    cnt = 0
    threshold = 0.1

    for d in data:

        if (
            _type == "TORUS"
            and round(abs(d["multiple_num"] - optimal_cell_size), 1) <= threshold
        ):
            cnt += 1

        if _type == "NO-TORUS" and d["multiple_num"] - threshold >= optimal_cell_size:
            cnt += 1
        elif _type == "NO-TORUS":
            print(d["multiple_num"] - threshold, d["multiple_num"])

    score = cnt / len(data)

    result = sorted([d["multiple_num"] for d in data])
    print("optimal", optimal_cell_size, "result", result[len(data) // 2], score)

    if score < 0.75:
        print("error", _type, score)

    return cnt / len(data)


def main():
    _dir = "./journal/data/weighting_gss/*"
    _dirs = [d + "/log/*" for d in glob.glob(_dir)]

    _dirs = [
        # "./journal/data/weighting_gss/gss_weighted_networkx0915_iteration10_loop15_0-5/log/*"
        # "./journal/data/weighting_gss/gss_randomPartition0920/log/*",
        # "./journal/data/weighting_gss/gss_weighted_random0915_iteration10_loop15_0-5/log/*",
        "./journal/data/weighting_gss/gss_regenerate_dought0920/log/*",
        "./journal/data/weighting_gss/gss_weighted_dough0915_iteration10_loop15_0-5/log/*",
        # "./journal/data/weighting_gss/gss_sparse0928/log/*",
        # "./journal/data/weighting_gss/gss_weighted_sparse0915_iteration10_loop15-0-5/log/*",
        # "./random_test_1014_gss/log/*",
    ]

    liner_files = glob.glob("./journal/data/weigthing_liner/*")

    with open("./graphSet0920/info_weigthed.json") as f:
        _graph_info = [g for g in json.load(f).values()]
    graph_info = list2dict(_graph_info)

    for lf in liner_files:
        logs = glob.glob(lf + "/log/*")
        for log in logs:
            name = re.split("[/]", log)[-1][:-6]
            if not name in graph_info:
                continue
            with open(log) as f:
                data = json.load(f)

            if graph_info[name]["type"] == "a":
                graph_info[name]["type"] = "NO-TORUS"
            else:
                graph_info[name]["type"] = "TORUS"

            graph_info[name]["optimal_cell_size"] = data["optimal_cell_size"]
            if graph_info[name]["type"] == "NO-TORUS":
                graph_info[name]["optimal_cell_size"] = get_decreas_stop_size(
                    data["data"], data["optimal_cell_size"]
                )
    result = []

    for d in _dirs:
        files = glob.glob(d)
        for filepath in files:
            print(filepath)
            with open(filepath) as f:
                data = json.load(f)
            name = re.split("[/]", filepath)[-1][:-10]
            if not name in graph_info:
                print("skip", name)
                continue
            print(name, "------------------")
            score = get_score(
                data, graph_info[name]["type"], graph_info[name]["optimal_cell_size"]
            )
            result.append([score, graph_info[name]["type"]])
            print(name, score)

    print(result)
    print(len(result))
    cnt = 0
    for r in result:
        if r[1] == "TORUS":
            cnt += 1
    print("TORUS", cnt, "NO-TORUS", len(result) - cnt)

    df = pd.DataFrame(result, columns=["Value", "Type"])

    plt.figure(figsize=(6, 8))
    sns.boxplot(x="Value", data=df, color="white")
    plt.show()

    plt.figure(figsize=(6, 8))
    sns.boxplot(x="Value", y="Type", data=df, color="white")
    plt.show()


if __name__ == "__main__":
    main()
