import collections
import copy
import networkx as nx
import matplotlib.pyplot as plt
import itertools
"""
networkx使って出す方
"""
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
    
    # ネットワーク生成
    G = nx.Graph()
    
    node_cnt = len(hakimi_degrees[-1])
    for i in range(node_cnt):
        G.add_node(i)
    
    data = [G]

    for i in range(len(hakimi_degrees)-2, -1, -1):
        print("--------")
        print(hakimi_degrees[i], i)
        G.add_node(node_cnt)

         # 増やさないといけないノードの次数
        add_node_degree = get_add_node_degree(hakimi_degrees[i+1], hakimi_degrees[i][1:])

        patern = []
        print(len(data))
        while len(data) > 0:
            g = data.pop(0)
            add_edge_nodes = get_edge_patern(g.degree, add_node_degree, node_cnt)
            print("add_edge_nodes", len(add_edge_nodes), add_edge_nodes, "g", g.edges)
            # for nodes in add_edge_nodes:
            for j in range(min(5, len(add_edge_nodes))):
                nodes = add_edge_nodes[j]
                g_copy = g.copy()
                for j in range(len(nodes)):
                    g_copy.add_edge(node_cnt, nodes[j])
                
                if len(patern):
                    for p in patern:
                        if not nx.is_isomorphic(g_copy, p):
                            patern.append(g_copy)
                else:
                    patern.append(g_copy)
            
            
            # for p in range(1,len(patern)):
            #     print(nx.is_isomorphic(patern[0], patern[p]))
            

        
        print("patern", len(patern))
        # exit()


        # test = [list(_g.edges) for _g in patern]
        # print(len(list(set(test))))



        print(len(list(set(patern))))
        for j in range(len(patern)):
            print(patern[j].nodes, patern[j].edges)
        
        data = patern[:5]
        node_cnt += 1
        # if(i)==2:
        #     exit()
        # print(node_cnt)
        # exit()
    exit()    
    nx.draw(G, with_labels=True)
    plt.show()


def get_degree(v, edges):
    cnt = 0
    for edge in edges:
        if v in edge:
            cnt += 1
    return cnt

def get_edge_patern(graph,  degrees, rm_node):
    koho = []
    for d in degrees:
        k = [node for node, edges in graph if edges == d and node!=rm_node]
        koho.append(k) 
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