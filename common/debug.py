
NODE_A = []
NODE_B = []
INDEX_A = []
INDEX_B = []


def clear():
    global NODE_A, NODE_B, INDEX_A, INDEX_B
    NODE_A = []
    NODE_B = []
    INDEX_A = []
    INDEX_B = []


def add_node_a(pos):
    global NODE_A
    NODE_A = pos


def add_node_b(pos):
    global NODE_B
    NODE_B = pos


def compare_node_pos():
    count = 0
    for i in range(len(NODE_A)):
        if NODE_A[i][0] != NODE_B[i][0] or NODE_A[i][1] != NODE_B[i][1]:
            if abs(NODE_A[i][0]-NODE_B[i][0]) > 0.0000001:
                print(NODE_A[i][0]-NODE_B[i][0])
            elif abs(NODE_A[i][1]-NODE_B[i][1]) > 0.0000001:
                print(NODE_A[i][1]-NODE_B[i][1])

            count += 1
    print("node", count/len(NODE_A), count, len(NODE_A))


def add_index_a(pos):
    global INDEX_A
    INDEX_A = pos


def add_index_b(pos):
    global INDEX_B
    INDEX_B = pos


def compare_index():
    count = 0
    for i in range(len(INDEX_A)):
        if INDEX_A != INDEX_B:
            count += 1
    print("index", count/len(INDEX_A), count, len(INDEX_A))
