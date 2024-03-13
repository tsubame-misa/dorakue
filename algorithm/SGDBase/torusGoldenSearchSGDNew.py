import setup
from algorithm.SGDBase import torusSGD
from common import log
import matplotlib.pyplot as plt
import math
import os
import shutil

"""
torusでstressを最も低くするlenghtを求める
(maxdを何倍したものがstressが低くなるか)
"""
def convertPos(pos, multiple_num, pre_multiple_num):
    # 倍率
    n = multiple_num/pre_multiple_num
    return [[x*n, y*n] for [x, y] in pos]
   


def get_midium_graph(graph, file_name, multiple_num, loop_value):
    """
    return 中央値を取るグラフ, bestなグラフ, bestなグラフのid
    """
    all_log = dict()
    stress = []
    for j in range(loop_value):
        time = setup.get_time()
        index_time = str(j) + str(time)
        _log =  torusSGD.torus_sgd(graph, file_name, multiple_num=multiple_num, time=index_time)
        all_log[index_time] = _log
        stress.append([index_time, _log["stress"]])

    sorted_stress = sorted(stress,  key=lambda x: x[1])
    return all_log[sorted_stress[len(sorted_stress)//2][0]], all_log[sorted_stress[0][0]], sorted_stress[0][0] 


def get_torus_graph(graph, file_name, multiple_num, pos=None, pre_multiple_num=None, use_pre_pos = 0, x=0.1, loop=5, _eta = None):
    time = setup.get_time()
    index_time = "0" + str(time)
    if pos and use_pre_pos==2:
        pos = convertPos(pos, multiple_num, pre_multiple_num)

    _log =  torusSGD.torus_sgd(graph, file_name, multiple_num=multiple_num, time=index_time, pre_pos = pos, _eta=True, start_idx=x)
    
    return _log, _log, index_time


def show_stress_graph(x, y, file_name):
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    plt.plot(x, y, marker='o',
             label='stress', linestyle='-', color='r')
    
    # ラベルやタイトルの設定
    plt.xlabel('cell size')
    plt.title(file_name)
    plt.legend()  # 凡例を表示

    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/stress_by_len/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_path = './' + dir_name+'/stress_by_len/' + file_name+'.png'
    plt.savefig(img_path)


def save_best_graph(best_graph_time, best_log, file_name, multipl_number):
    dir_name = setup.get_dir_name()
    new_dir_path = './' + dir_name + "/best/" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    # 画像の保存
    new_dir_path = './' + dir_name + "/best/img" 

    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    img_file_name = file_name + "-" + str(multipl_number) + "-" + best_graph_time + ".png"
    
    shutil.copyfile(dir_name + "/torusSGD_wrap/" + img_file_name, new_dir_path+ "/" + img_file_name)  
    print("saved", new_dir_path+ "/" + img_file_name)

    # ログの保存
    best_log["multipl_number"] = multipl_number
    log.create_log(best_log, file_name+"-best")


def debug_log(data, all_log, file_name):
    sorted_data = sorted(data, key=lambda x: x[0])
    print(sorted_data)

    log.create_log(all_log, file_name)

    show_stress_graph([row[0] for row in sorted_data],[row[1] for row in sorted_data], file_name)




"""
use_pre_pos
0:no use, 1:use pre pose, 2:use scaled pre pos
"""
def torus_golden_search_new(graph, file_name, log_file_name="test", avg_loog = 20,  use_pre_pos = 0, debug=False, index=0):
    count = 20

    low = 0
    high = 3

    lr_diff = high-low
    x = (3-math.sqrt(5))/2*lr_diff
    low_multipl_number = x
    high_multipl_number = high - x

    low_graph, low_best_graph, low_best_graph_time = get_midium_graph(graph, file_name, low_multipl_number, avg_loog)
    high_graph, high_best_graph, high_best_graph_time = get_midium_graph(graph, file_name, high_multipl_number, avg_loog)
    pre_multipl_number = 1

    data = [[low_multipl_number, low_graph["stress"]],[high_multipl_number, high_graph["stress"]]]
    all_log = {"file": file_name}
    
    for i in range(1, count):
        print(i, low, high)
        """
        計算量をなんとかしたい
        1. ここを中央値にする(最低ライン)
        2. 広い領域で描画した結果を狭い領域での描画に使いまわしたい(逆も)
         - 初期配置を、前のものを使う
         - 連続性を期待するため、中央値は取らない。一回だけやる
         - 3分に限らずでも
        """
            
        if low_graph["stress"] > high_graph["stress"]:
            data.append([low_multipl_number, low_graph["stress"]])
            all_log[low_multipl_number] = {"1":{"torusSGD":low_graph}}

            low = low_multipl_number
            low_multipl_number = high_multipl_number
            high_multipl_number = high - (lr_diff-2*x)

            low_graph = high_graph
            low_best_graph = high_best_graph
            low_best_graph_time = high_best_graph_time  
            # print("x", x)
            if use_pre_pos > 0:  
                high_graph, high_best_graph, high_best_graph_time = \
                    get_torus_graph(graph, file_name, high_multipl_number, pos=high_best_graph["pos"], 
                                    pre_multiple_num=pre_multipl_number, use_pre_pos=use_pre_pos, x=i)
                low_graph, low_best_graph, low_best_graph_time = \
                    get_torus_graph(graph, file_name, low_multipl_number, pos=high_best_graph["pos"], 
                                    pre_multiple_num=pre_multipl_number, use_pre_pos=use_pre_pos, x=i)
            else:
                high_graph, high_best_graph, high_best_graph_time = get_midium_graph(graph, file_name, high_multipl_number, avg_loog)
            pre_multipl_number = high_multipl_number
        else:
            data.append([high_multipl_number, high_graph["stress"]])
            all_log[high_multipl_number] = {"2":{"torusSGD":high_graph}}

            high = high_multipl_number
            high_multipl_number = low_multipl_number
            low_multipl_number = low + lr_diff-2*x

            high_graph = low_graph
            high_best_graph = low_best_graph
            high_best_graph_time = low_best_graph_time
            if use_pre_pos:
                low_graph, low_best_graph, low_best_graph_time = \
                    get_torus_graph(graph, file_name, low_multipl_number, pos=low_best_graph["pos"], 
                                    pre_multiple_num=pre_multipl_number, use_pre_pos=use_pre_pos, x=i)
                high_graph, high_best_graph, high_best_graph_time = \
                    get_torus_graph(graph, file_name, high_multipl_number, pos=low_best_graph["pos"], 
                                    pre_multiple_num=pre_multipl_number, use_pre_pos=use_pre_pos, x=i)
            else:
                low_graph, low_best_graph, low_best_graph_time = get_midium_graph(graph, file_name, low_multipl_number, avg_loog)
            pre_multipl_number = low_multipl_number
        
        lr_diff = high-low
        x = (3-math.sqrt(5))/2*lr_diff
        
        if abs(low_multipl_number-high_multipl_number) < 0.001:
            break
    
    if low_graph["stress"] > high_graph["stress"]:
        data.append([high_multipl_number, high_graph["stress"]])
        print("min", high_multipl_number)
        all_log["best"] = high_best_graph
        save_best_graph(high_best_graph_time, high_best_graph, file_name, high_multipl_number)
        if debug:
            debug_log(data, all_log, file_name+str(index))
        # new_graph, best_graph, graph_time =  get_torus_graph(graph, file_name, high_multipl_number, pos=high_graph["pos"], 
        #                             pre_multiple_num=pre_multipl_number, use_pre_pos=use_pre_pos, loop=15)
        new_graph, best_graph, graph_time =  get_midium_graph(graph, file_name, high_multipl_number, avg_loog)
        # return high_graph
        return best_graph
    else:
        data.append([low_multipl_number, low_graph["stress"]])
        print("min", low_multipl_number)
        all_log["best"] = low_best_graph
        save_best_graph(low_best_graph_time, low_best_graph, file_name, low_multipl_number)
        if debug:
            debug_log(data, all_log, file_name+str(index))
        # new_graph, best_graph, graph_time =  get_torus_graph(graph, file_name, low_multipl_number, pos=low_graph["pos"], 
        #                             pre_multiple_num=pre_multipl_number, use_pre_pos=use_pre_pos, x=15)
        new_graph, best_graph, graph_time =  get_midium_graph(graph, file_name, high_multipl_number, avg_loog)
        # return low_graph
        return best_graph