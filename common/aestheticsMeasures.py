import calcDrawInfo


def calc_mean(array):
    return sum(array)/len(array)


def calc_sd(array):
    mean = calc_mean(array)
    return sum((score - mean)**2 for score in array)/len(array)


def calc_evaluation_values(delta, dist_score):
    delta_mean = calc_mean(delta)
    delta_sd = calc_sd(delta)
    delta_sum = sum(delta)

    dist_mean = calc_mean(dist_score)
    dist_sd = calc_sd(dist_score)
    dist_sum = sum(dist_score)

    return {"delta": {"mean": delta_mean, "sd": delta_sd, "sum": delta_sum},
            "dist": {"mean": dist_mean, "sd": dist_sd, "sum": dist_sum}}


def calc_edge_length_variance(pos, graph, node2num):
    l = []
    for x_node, y_node in graph.edges:
        u = node2num[x_node]
        v = node2num[y_node]
        l.append(calcDrawInfo.dist(pos, u, v))
    l_mean = calc_mean(l)
    variance = sum([((l_mean/l_mean) - (l[i]/l_mean))
                   ** 2 for i in range(l)])/len(l)
    return variance
