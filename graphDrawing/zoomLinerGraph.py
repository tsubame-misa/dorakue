import glob
from networkx.readwrite import json_graph
import json
import re
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def main():
    cell_size_files = glob.glob("./graphDrawing/data/egraph/liner_egraph_networkx_20/log/save_best_len_log/*")
    
    for filepath in cell_size_files:
        with open(filepath) as f:
            data = json.load(f)
        file_name = re.split('[/]', filepath)[-1][:-6]

        if not (file_name=="house_x" or file_name=="tutte" or file_name=="sedgewick_maze"):
            continue

        plt.figure(figsize=(8, 6))  # グラフのサイズを設定
        plt.plot(data["x"][20:-30], data["y"][20:-30], marker='',
                label='stress', linestyle='-', color='r', )
        
        # ラベルやタイトルの設定
        plt.xlabel('How many times maxd')
        plt.ylabel('stress')
        plt.title(file_name) 
        plt.show()
       
    
    

if __name__ == '__main__':
    main()