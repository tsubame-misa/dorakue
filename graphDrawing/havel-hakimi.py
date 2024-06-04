import networkx as nx
import matplotlib.pyplot as plt

def hakimi(deg, data):
    sorted_deg = sorted(deg, reverse=True)

    n = len(sorted_deg)
    l = sorted_deg.pop(0)

    if l == 0:           return True
    if l < 0:            return False
    if l > 0 and n == 1: return False

    for i in range(l):
        sorted_deg[i] -= 1
    data.append(sorted(sorted_deg, reverse=True))

    return hakimi(sorted_deg, data)
    

def get_add_node_degree(before, after):
    print("b",before)
    print("a",after)
    add_node_degree = []
    for i in range(len(before)):
        if after[i] - before[i] == 1:
            add_node_degree.append(before[i])
    return add_node_degree


def get_edge(G, degree):
    for v in G:
        if G.degree(v) == degree:
            return v

def create_graph(degrees):
    hakimi_degrees = [degrees] 
    hakimi(degrees, hakimi_degrees)
    # hakimi_degrees = [[6,5,5,4,3,3,2,2,2], [4, 4, 3, 2, 2, 2, 2, 1], [3, 2, 2, 2, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0]]
    print(hakimi_degrees)
    # ネットワーク生成
    G = nx.Graph()
    
    node_cnt = len(hakimi_degrees[-1])
    for i in range(node_cnt):
        G.add_node(i)

    for i in range(len(hakimi_degrees)-2, -1, -1):
        print(hakimi_degrees[i], i)
        G.add_node(node_cnt)
        
        # 増やさないといけないノードの次数
        add_node_degree = get_add_node_degree(hakimi_degrees[i+1], hakimi_degrees[i][1:])
        for j in range(hakimi_degrees[i][0]):
            connect_edge = get_edge(G, add_node_degree[j])
            print("connect_edge", connect_edge)
            G.add_edge(node_cnt, connect_edge)
        
        node_cnt += 1
    nx.draw(G, with_labels=True)
    plt.show()


def get_edge(G, degree):
    for v in G:
        if G.degree(v) == degree:
            return v
    

    
    # nx.draw(G, with_labels=True)
    # plt.show()




if __name__ == '__main__':
    create_graph([3,3,3,3,3,1])
    create_graph([6,5,5,4,3,3,2,2,2])