import glob
import json
import matplotlib.pyplot as plt
import seaborn as sns
import re


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

    graph_info = list2dict(_graph_info)

    for key in graph_info.keys():
        graph_info[key]["append"] = False

    cell_size = []
    for files_name in log_files:
        files = glob.glob(files_name)
        for file in files:
            file_name = re.split("[/]", file)[-1][:-6]
            if not file_name in graph_info or graph_info[file_name]["append"]:
                continue
            print(file_name)
            with open(file) as f:
                data = json.load(f)
            if rename:
                optimal = data["optimal_cell_size"]
                graph_info[file_name]["append"] = True
                cell_size.append(optimal)
            else:
                print(file)
                cell_size.append(data["best_multiple_num"])
                graph_info[file_name]["append"] = True

    print(len(cell_size))
    sns.histplot(cell_size, bins=12, color="skyblue", edgecolor="black")
    plt.xlabel("How many times the diameter")
    plt.ylabel("Frequency")
    plt.xlim(left=0)
    plt.title("Histogram of optimal cell size")
    plt.show()


if __name__ == "__main__":
    main()
