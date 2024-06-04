import collections
import copy
import networkx as nx
import matplotlib.pyplot as plt
import itertools

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

    print(hakimi_degrees)

    nodes = []
    node_cnt = len(hakimi_degrees[-1])
    graph = dict()
    for i in range(node_cnt):
        graph[i] = []

    data = [graph]

    # for i in range(len(hakimi_degrees)-2, -1, -1):
    for i in range(len(hakimi_degrees)-2, 0, -1):
        nodes.append(node_cnt)

        print("--------")
         # 増やさないといけないノードの次数
        add_node_degree = get_add_node_degree(hakimi_degrees[i+1], hakimi_degrees[i][1:])
        
         
        print(hakimi_degrees[i], i, "node_cnt", node_cnt, "add_node_degree", add_node_degree)

        patern = []
        print(len(data))
        while len(data) > 0:
            g = data.pop(0)
            add_edge_nodes = get_edge_patern(g,add_node_degree, node_cnt)

            for nodes in add_edge_nodes:
                new_g = copy.deepcopy(g)
                for n in nodes:
                    new_g[n].append((node_cnt, n))
                    if not node_cnt in new_g:
                        new_g[node_cnt] = []
                    new_g[node_cnt].append((node_cnt, n))
                patern.append(new_g)
        
        print("patern", len(patern))

        data = patern
        node_cnt += 1

        if i==2:
            exit()

    print("##############")
    final = []
    for p in patern:
        print("p",p)
        littleG = nx.DiGraph()  # 有向グラフ (Directed Graph)
        littleG.add_nodes_from(p.keys())
        littleG.add_edges_from(sum(p.values(), []))
        if len(final):
            for f in final:
                if not nx.is_isomorphic(littleG, f):
                    final.append(littleG)
        else:
            final.append(littleG)
    
    print(len(final))


def get_degree(v, edges):
    cnt = 0
    for edge in edges:
        if v in edge:
            cnt += 1
    return cnt

def get_edge_patern(graph,  degrees, rm_node):
    # print(graph, degrees, rm_node)
    koho = []
    for d in degrees:
        k = [node for node, edges in graph.items() if len(edges)== d and node!=rm_node]
        koho.append(k) 
    print("koho",koho)
    koho_combination = list(itertools.product(*koho))
    add_edge_nodes = []
    for k in koho_combination:
        c = collections.Counter(k).most_common()[0][1]
        if c==1:
            add_edge_nodes.append(list(k))
    return add_edge_nodes



def get_edge(G, degree):
    for v in G:
        if G.degree(v) == degree:
            return v



if __name__ == '__main__':
    # G = nx.path_graph(4)  # or DiGraph, MultiGraph, MultiDiGraph, etc
    # nx.draw(G, with_labels=True)
    # plt.show()
    # H = G.copy()
    # H.add_edge(0, 3)
    # nx.draw(H, with_labels=True)
    # plt.show()
    # create_graph([3,3,3,3,3,1])
    create_graph([6,5,5,4,3,3,2,2,2])