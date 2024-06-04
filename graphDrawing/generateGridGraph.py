import networkx as nx # NetworkXをインポート

# ネットワーク生成
G = nx.Graph([(1, 2), (2, 3), (3, 1)])

n = 3
edges = []
for i in range(n):
    for j in range(n):
        a = [(i, i+1)]
# G = nx.Graph() # 空のグラフを作成する場合
nx.draw(G, with_labels=True) # ラベルをTrueにして番号の可視化