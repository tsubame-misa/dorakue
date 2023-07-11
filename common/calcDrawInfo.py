import math

DORAKUE = False


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


def dist(pos, u, v):
    dx = pos[u][0] - pos[v][0]
    dy = pos[u][1] - pos[v][1]
    return (dx ** 2 + dy ** 2) ** 0.5


def dist_around(pos, u, v, width, height):
    # uが中心
    d = dist(pos, u, v)

    ax = pos[u][0] - ((pos[v][0]-(pos[u][0]-width/2) +
                       width) % width+(pos[u][0]-width/2))
    ay = pos[u][1] - ((pos[v][1]-(pos[u][1]-height/2) +
                       height) % height+(pos[u][1]-height/2))
    adist = (ax ** 2 + ay ** 2) ** 0.5
    return min(d, adist)


def dist_around_position(pos, u, v, width, height):
    # # 回り込みが発生しない場合
    d = dist(pos, u, v)
    d_around = dist_around(pos, u, v, width, height)
    # # print(d, d_around)
    # if d == d_around:
    #     return [pos[u][0]-pos[v][0], pos[u][1]-pos[v][1]]
    # else:
    #     print("around")
    # if abs(pos[u][0]-pos[v][0]) < 0.0000001 and abs(pos[u][1]-pos[v][1]) < 0.0000001:
    #     return [pos[u][0]-pos[v][0], pos[u][1]-pos[v][1]]
    if abs(d-d_around) < 0.00000001:
        return [pos[u][0]-pos[v][0], pos[u][1]-pos[v][1]]
    # print(abs("around", d-d_around))
    # uが中心
    ax = pos[u][0] - ((pos[v][0]-(pos[u][0]-width/2) +
                       width) % width+(pos[u][0]-width/2))
    ay = pos[u][1] - ((pos[v][1]-(pos[u][1]-height/2) +
                       height) % height+(pos[u][1]-height/2))
    return [ax, ay]


def dorakue(pos, width, height):
    global DORAKUE
    # 先生の式のやつでやらないとダメかも？
    if pos[0] < 0:
        pos[0] = width*(abs(pos[0])//width+1)+pos[0]
        # print("dorakue")
        DORAKUE = True
    elif pos[0] > width:
        pos[0] = pos[0]-width*(abs(pos[0])//width)
        # print("dorakue")
        DORAKUE = True

    if pos[1] < 0:
        pos[1] = height*(abs(pos[1])//height+1)+pos[1]
        # print("dorakue")
        DORAKUE = True
    elif pos[1] > height:
        pos[1] = pos[1]-height*(abs(pos[1])//height)
        # print("dorakue")
        DORAKUE = True

    return pos


def shift_center(pos, idx, node_len, width, height):
    diff_x = pos[idx][0]-width/2
    diff_y = pos[idx][1]-height/2

    for i in range(node_len):
        pos[i][0] -= diff_x
        pos[i][1] -= diff_y
        pos[i] = dorakue(pos[i], width, height)

    return diff_x, diff_y, pos


def shift_flat(pos, diff_x, diff_y, node_len, width, height):
    for i in range(node_len):
        pos[i][0] += diff_x
        pos[i][1] += diff_y

        pos[i] = dorakue(pos[i], width, height)

    return pos


def calc_delta(pos,  k, l, node_len):
    Delta = [0]*node_len
    for i in range(node_len):
        Ex = 0
        Ey = 0
        for j in range(node_len):
            if i == j:
                continue
            norm = math.sqrt((pos[i][0]-pos[j][0]) **
                             2 + (pos[i][1]-pos[j][1])**2)
            dx_ij = pos[i][0]-pos[j][0]
            dy_ij = pos[i][1]-pos[j][1]

            Ex += k[i][j]*dx_ij*(1.0-l[i][j]/norm)
            Ey += k[i][j]*dy_ij*(1.0-l[i][j]/norm)
        Delta[i] = math.sqrt(Ex*Ex+Ey*Ey)
    return Delta


def get_max_delta(pos,  k, l, node_len):
    delta = calc_delta(pos,  k, l, node_len)
    return delta.index(max(delta))


def get_max_around_delta(pos,  k, l, node_len, width, height):
    delta = calc_delta_around(pos,  k, l, node_len, width, height)
    return delta.index(max(delta))


def calc_delta_around(pos,  k, l, node_len, width, height):
    Delta = [0]*node_len
    for i in range(node_len):
        Ex = 0
        Ey = 0
        _pos = [[x, y] for x, y in pos]
        diff_x, diff_y, _pos = shift_center(
            _pos, i, node_len, width, height)
        for j in range(node_len):
            if i == j:
                continue
            norm = math.sqrt((_pos[i][0]-_pos[j][0]) **
                             2 + (_pos[i][1]-_pos[j][1])**2)
            dx_ij = _pos[i][0]-_pos[j][0]
            dy_ij = _pos[i][1]-_pos[j][1]

            Ex += k[i][j]*dx_ij*(1.0-l[i][j]/norm)
            Ey += k[i][j]*dy_ij*(1.0-l[i][j]/norm)
        Delta[i] = math.sqrt(Ex*Ex+Ey*Ey)
    return Delta


def clear_dorakue():
    global DORAKUE
    DORAKUE = False


def get_has_dorakue():
    return DORAKUE
