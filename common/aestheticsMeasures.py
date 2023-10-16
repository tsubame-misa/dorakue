from common import calcDrawInfo
import math
import numpy as np
import itertools


def calc_mean(array):
    return sum(array)/len(array)


def calc_sd(array):
    mean = calc_mean(array)
    return sum((score - mean)**2 for score in array)/len(array)


def calc_evaluation_values(delta, dist_score, graph, node2num, pos, l, width=None, height=None, isTorus=False):
    delta_mean = calc_mean(delta)
    delta_sd = calc_sd(delta)
    delta_sum = sum(delta)

    dist_mean = calc_mean(dist_score)
    dist_sd = calc_sd(dist_score)
    dist_sum = sum(dist_score)

    edge_length_variance = calc_edge_length_variance(pos, graph, node2num)
    minimum_angle = calc_minimum_angle(pos, l)
    edge_crossings, wrap = calc_edge_crossings(graph, node2num, pos)

    return {"delta": {"mean": delta_mean, "sd": delta_sd, "sum": delta_sum},
            "dist": {"mean": dist_mean, "sd": dist_sd, "sum": dist_sum},
            "edge_length_variance": edge_length_variance,
            "minimum_angle": minimum_angle,
            "edge_crossings": edge_crossings}


def calc_torus_evaluation_values(delta, dist_score, graph, node2num, pos, l, _len):
    delta_mean = calc_mean(delta)
    delta_sd = calc_sd(delta)
    delta_sum = sum(delta)

    dist_mean = calc_mean(dist_score)
    dist_sd = calc_sd(dist_score)
    dist_sum = sum(dist_score)

    edge_length_variance = calc_edge_length_variance(
        pos, graph, node2num, l, _len, True)
    minimum_angle = calc_minimum_angle(pos, l, _len, True)
    edge_crossings, wrap = calc_edge_crossings(
        graph, node2num, pos, l, _len, True)

    return {"delta": {"mean": delta_mean, "sd": delta_sd, "sum": delta_sum},
            "dist": {"mean":
                     dist_mean, "sd": dist_sd, "sum": dist_sum},
            "edge_length_variance": edge_length_variance,
            "minimum_angle": minimum_angle,
            "edge_crossings": edge_crossings,
            "wrap": wrap}


def calc_edge_length_variance(pos, graph, node2num, _l=None, _len=0, torus=False):
    l = []
    for x_node, y_node in graph.edges:
        u = node2num[str(x_node)]
        v = node2num[str(y_node)]
        if torus:
            l.append(calcDrawInfo.dist_around(pos, u, v, _len, _len, _l[u][v]))
        else:
            l.append(calcDrawInfo.dist(pos, u, v))

    l_mean = calc_mean(l)
    variance = sum([((l_mean/l_mean) - (l[i]/l_mean))
                   ** 2 for i in range(len(l))])/len(l)
    return variance


def select_node(pos, u, v, _len, ideal_dist):
    # uから見た
    x_list = [pos[v][0]-_len, pos[v][0], pos[v][0]+_len]
    y_list = [pos[v][1]-_len, pos[v][1], pos[v][1]+_len]

    squea_side_edge = [[[0, 0], [0, _len]], [[0, 0], [_len, 0]], [
        [_len, 0], [_len, _len]], [[_len, _len], [0, _len]]]

    best_pos = [pos[v][0], pos[v][1]]
    _dist = float("inf")

    for x in x_list:
        for y in y_list:
            ax = pos[u][0] - x
            ay = pos[u][1] - y
            adist = (ax ** 2 + ay ** 2) ** 0.5
            if abs(_dist-ideal_dist) > abs(adist-ideal_dist):
                best_pos[0] = x
                best_pos[1] = y
                _dist = adist

    is_wrap = not(best_pos[0] == pos[v][0] and best_pos[1] == pos[v][1])

    if is_wrap:
        for n1, n2 in squea_side_edge:
            if is_cross(n1, n2, pos[u], best_pos):
                best_pos = intersection(n1, n2, pos[u], best_pos)
                break

    return best_pos, is_wrap


def calc_deg(pos, u, v, l, _len, wrap=False):
    x0, y0 = 0, 0
    vec1 = [pos[u][0]-x0, pos[u][1]-y0]

    if wrap:
        best_pos, is_wrap = select_node(pos, u, v, _len, l[u][v])
        vec2 = [best_pos[0]-x0, best_pos[1]-y0]
    else:
        vec2 = [pos[v][0]-x0, pos[v][1]-y0]

    absvec1 = np.linalg.norm(vec1)
    absvec2 = np.linalg.norm(vec2)
    inner = np.inner(vec1, vec2)
    cos_theta = inner/(absvec1*absvec2)
    theta = math.degrees(math.acos(cos_theta))
    return theta


def calc_minimum_angle(pos, l, _len=0, wrap=False):
    _sum = 0
    for i in range(len(pos)):
        # 近接ノード
        near_i = [j for j, x in enumerate(l[i]) if x == 100]
        # 理想の角度
        ideal_theta = 360/len(near_i)
        # ある点を基準に角度をとる
        thetas_from_zero = []
        thetas = []
        for v in near_i:
            thetas_from_zero.append(calc_deg(pos, i, v, l, _len, wrap))
        # ソートしないと隣同士の角度が取れないのでソート
        thetas_from_zero = sorted(thetas_from_zero, reverse=True)
        for j in range(1, len(thetas_from_zero)-1):
            thetas.append(thetas_from_zero[j+1]-thetas_from_zero[j])
        thetas.append(thetas_from_zero[0]+(360-thetas_from_zero[-1]))
        min_theta = min(thetas)
        _sum += abs(ideal_theta-min_theta)/ideal_theta
    return _sum/len(pos)


def is_cross(p1, p2, p3, p4):
    tc1 = (p1[0] - p2[0]) * (p3[1] - p1[1]) + (p1[1] - p2[1]) * (p1[0] - p3[0])
    tc2 = (p1[0] - p2[0]) * (p4[1] - p1[1]) + (p1[1] - p2[1]) * (p1[0] - p4[0])
    td1 = (p3[0] - p4[0]) * (p1[1] - p3[1]) + (p3[1] - p4[1]) * (p3[0] - p1[0])
    td2 = (p3[0] - p4[0]) * (p2[1] - p3[1]) + (p3[1] - p4[1]) * (p3[0] - p2[0])
    return tc1*tc2 < 0 and td1*td2 < 0


def is_cross_pos(p1, p2, p3, p4):
    tc1 = (p1 - p2) * (p3 - p1) + (p1 - p2) * (p1 - p3)
    tc2 = (p1 - p2) * (p4 - p1) + (p1 - p2) * (p1 - p4)
    td1 = (p3 - p4) * (p1 - p3) + (p3 - p4) * (p3 - p1)
    td2 = (p3 - p4) * (p2 - p3) + (p3 - p4) * (p3 - p2)
    return tc1*tc2 < 0 and td1*td2 < 0


# 2つの線分の交点を求める
def intersection(p1, p2, p3, p4):
    det = (p1[0] - p2[0]) * (p4[1] - p3[1]) - (p4[0] - p3[0]) * (p1[1] - p2[1])
    t = ((p4[1] - p3[1]) * (p4[0] - p2[0]) +
         (p3[0] - p4[0]) * (p4[1] - p2[1])) / det
    x = t * p1[0] + (1.0 - t) * p2[0]
    y = t * p1[1] + (1.0 - t) * p2[1]
    return x, y


def calc_edge_crossings(graph, node2num, pos, l=None, _len=0, wrap=False):
    count = 0
    is_wrap = False
    if wrap:
        torus_edges = torus_edge_pair(graph, node2num,  pos, l,  _len)
        edge_pair = [list(p) for p in itertools.combinations(torus_edges, 2)]

        if len(torus_edges) > len(graph.edges):
            is_wrap = True

        for i in range(len(edge_pair)):
            n1 = list(edge_pair[i][0][0])
            n2 = list(edge_pair[i][0][1])
            n3 = list(edge_pair[i][1][0])
            n4 = list(edge_pair[i][1][1])
            if is_cross(n1, n2, n3, n4):
                count += 1
    else:
        edge_pair = [list(p) for p in itertools.combinations(graph.edges, 2)]
        for i in range(len(edge_pair)):
            n1 = node2num[str(edge_pair[i][0][0])]
            n2 = node2num[str(edge_pair[i][0][1])]
            n3 = node2num[str(edge_pair[i][1][0])]
            n4 = node2num[str(edge_pair[i][1][1])]
            if is_cross(pos[n1], pos[n2], pos[n3], pos[n4]):
                count += 1
    return count, is_wrap


def torus_edge_pair(graph, node2num,  pos, l,  _len):
    edge_lines = []
    for i, j in graph.edges:
        idx_i = node2num[str(i)]
        idx_j = node2num[str(j)]

        best_pos, is_wrap = select_node(
            pos, idx_i, idx_j, _len, l[idx_i][idx_j])

        line = [(pos[idx_i][0], pos[idx_i][1]),
                (best_pos[0], best_pos[1])]
        edge_lines.append(line)

        if is_wrap:
            best_pos, is_wrap = select_node(
                pos,  idx_j, idx_i, _len, l[idx_j][idx_i])
            line = [(pos[idx_j][0], pos[idx_j][1]),
                    (best_pos[0], best_pos[1])]
            edge_lines.append(line)

    return edge_lines
