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
    # log_files = [f + "/log/*" for f in glob.glob("./journal/data/weigthing_liner/*")]
    log_files = [f + "/log/*" for f in glob.glob("./journal/data/liner/*")]

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
            optimal = data["optimal_cell_size"]
            graph_info[file_name]["append"] = True
            cell_size.append(optimal)

    print(len(cell_size))
    sns.histplot(cell_size, bins=12, color="skyblue", edgecolor="black")
    plt.xlabel("How many times the diameter")
    plt.ylabel("Frequency")
    plt.xlim(left=0)
    plt.title("Histogram of optimal cell size")
    plt.show()


if __name__ == "__main__":
    main()
