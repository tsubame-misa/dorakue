"""
線形探索した結果最適値がどう分布してるかを出してた
"""
import glob
import json
import matplotlib.pyplot as plt
import seaborn as sns



def crate_scatter_plt(x, y):
    plt.axhline(y=1, color='r', linestyle='--')
    plt.scatter(x)

    plt.xlabel('times')
    # plt.ylabel('compare stress')
    plt.title('')
    plt.legend()

    plt.show()


files = glob.glob("./test_stress_liner_avarage_20/log/save_best_len_log/*")

# scatter_x = []

# for filepath in files:
#     with open(filepath) as f:
#         data = json.load(f)
#     scatter_x.append(data["best_multiple_num"])

scatter_x = [2.25, 1.25, 1.5, 1.3, 1.2, 1.25, 1.25, 2.0, 3.35, 1.8, 3.55, 1.3, 1.5, 1.2, 2.15, 1.85, 1.35, 1.55, 1.55, 1.3, 2.05, 3.25]
plt.figure(figsize=(6, 2)) 

# Swarm plot
# sns.swarmplot(x=scatter_x, color='#1581ed', alpha=0.7)

# 箱ひげ図
sns.boxplot(x=scatter_x, color='white', width=0.2)

plt.xlabel("How many times the diameter")

print(scatter_x)


# グラフの表示
plt.show()