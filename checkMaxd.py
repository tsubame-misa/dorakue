import matplotlib.pyplot as plt
import glob
import json
import matplotlib.pyplot as plt
import setup
import re
import os
import matplotlib.image as mpimg

"""
maxdを変化させた場合の評価値の変化のグラフを表示する
"""


def generate_liner_graph(maxd_x, torus_maxd_y, maxd_y, file_name, dir_name, itemname):
    # プロット設定
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(maxd_x, maxd_y, marker='o',
             label='no-torus', linestyle='-', color='r')
    plt.plot(maxd_x, torus_maxd_y, marker='o',
             label='torus', linestyle='-', color='b')

    # ラベルやタイトルの設定
    plt.xlabel('How many times maxd')
    plt.ylabel(itemname)
    plt.title(file_name)
    plt.legend()  # 凡例を表示

    new_dir_path = './' + dir_name + "/maxd_check/" + itemname

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_path = './' + dir_name+'/maxd_check/' + itemname + "/" + file_name+'.png'
    plt.savefig(img_path)
    print(img_path)

    plt.clf()
    plt.close()

    return img_path


def create_compare_fig(images, filename, dir_name):
    fig = plt.figure(figsize=(12, 12))
    plt.title(filename)
    plt.axis("off")

    for i in range(len(images)):
        item_name = re.split('[/.-]', images[i])[-3]
        ax = fig.add_subplot(2, 3, i+1)
        ax.set_title(item_name, fontsize=10)
        ax.axes.xaxis.set_visible(False)  # X軸を非表示に
        ax.axes.yaxis.set_visible(False)  # Y軸を非表示に

        img = mpimg.imread(images[i])
        plt.imshow(img)

    new_dir_path = './' + dir_name + "/maxd_check/compare"

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    dir_name = setup.get_dir_name()
    img_path = new_dir_path + "/" + filename + ".png"
    plt.savefig(img_path)

    plt.clf()
    plt.close()


folder_name = "result_1117_detail"
# folder_name = "./past/result0718"
for filepath in glob.glob("./" + folder_name + "/log/*"):
    with open(filepath) as f:
        data = json.load(f)
        filename = re.split('[/.-]', filepath)[-3]
        maxd_x = list(data.keys())
        maxd_x.pop(0)

        maxd_y = []
        edge_crossing = []
        edge_length_variance = []
        minimum_angle = []
        node_resolution = []

        torus_maxd_y = []
        torus_edge_crossing = []
        torus_edge_length_variance = []
        torus_minimum_angle = []
        torus_node_resolution = []

        images = []

        for _len in maxd_x:
            stress_array = [data[_len][i]["SGD"]["delta"]["sum"]
                            for i in data[_len].keys()]
            stress_array = [data[_len][i]["SGD"]["stress"]
                            for i in data[_len].keys()]
            crossing = [data[_len][i]["SGD"]["edge_crossings"]
                        for i in data[_len].keys()]
            edge_length_v = [data[_len][i]["SGD"]["edge_length_variance"]
                             for i in data[_len].keys()]
            min_angle = [data[_len][i]["SGD"]["minimum_angle"]
                         for i in data[_len].keys()]
            _node_resolution = [data[_len][i]["SGD"]["node_resolution"]
                         for i in data[_len].keys()]

            maxd_y.append(sum(stress_array)/len(stress_array))
            edge_crossing.append(sum(crossing)/len(crossing))
            edge_length_variance.append(sum(edge_length_v)/len(edge_length_v))
            minimum_angle.append(sum(min_angle)/len(min_angle))
            node_resolution.append(sum(_node_resolution)/len(_node_resolution))

            stress_array = [data[_len][i]["torusSGD"]["delta"]["sum"]
                            for i in data[_len].keys()]
            stress_array = [data[_len][i]["torusSGD"]["stress"]
                            for i in data[_len].keys()]
            crossing = [data[_len][i]["torusSGD"]["edge_crossings"]
                        for i in data[_len].keys()]
            edge_length_v = [data[_len][i]["torusSGD"]["edge_length_variance"]
                             for i in data[_len].keys()]
            min_angle = [data[_len][i]["torusSGD"]["minimum_angle"]
                         for i in data[_len].keys()]
            _node_resolution = [data[_len][i]["torusSGD"]["node_resolution"]
                         for i in data[_len].keys()]
            
            torus_maxd_y.append(sum(stress_array)/len(stress_array))
            torus_edge_crossing.append(sum(crossing)/len(crossing))
            torus_edge_length_variance.append(
                sum(edge_length_v)/len(edge_length_v))
            torus_minimum_angle.append(sum(min_angle)/len(min_angle))
            torus_node_resolution.append(sum(_node_resolution)/len(_node_resolution))

    # print()
    # print(maxd_x)
    # print(torus_maxd_y)
    # print(maxd_y)
    # print(filepath)
    # maxd_x = [0.25, 0.5,  0.75,  1, 2**0.5, 2, 3, 4, 5, 6, 7, 8, 9]
    maxd_x = [0.2, 0.4,  0.6, 0.8, 1, 1.2, 1.4, 1.6,1.8,2]
    # generate_liner_graph(maxd_x[:6], torus_maxd_y[:6],
    #                      maxd_y[:6], filename, folder_name)

    new_dir_path = './' + folder_name + "/maxd_check/"

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)
    images.append(generate_liner_graph(maxd_x, torus_maxd_y, maxd_y,
                                       filename, folder_name, "stress"))
    images.append(generate_liner_graph(maxd_x, torus_edge_crossing, edge_crossing,
                                       filename, folder_name, "edge_crossing"))
    images.append(generate_liner_graph(maxd_x, torus_edge_length_variance, edge_length_variance,
                                       filename, folder_name, "edge_length_variance"))
    images.append(generate_liner_graph(maxd_x, torus_minimum_angle, minimum_angle,
                                       filename, folder_name, "minimum_angle"))
    images.append(generate_liner_graph(maxd_x, torus_node_resolution, node_resolution,
                                       filename, folder_name, "node_resolution"))
    create_compare_fig(images, filename, folder_name)
