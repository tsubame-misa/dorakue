import math

DORAKUE = False


def dist(pos, u, v):
    dx = pos[u][0] - pos[v][0]
    dy = pos[u][1] - pos[v][1]
    return (dx ** 2 + dy ** 2) ** 0.5


def dist_around(pos, u, v, width, height, ideal_dist,  use_ideal=False):
    _dist, best_pos, is_wrap = dist_around9(
        pos, u, v, width, height, ideal_dist, False)
    return _dist


def dist_around9(pos, u, v, width, height, ideal_dist, use_ideal=False):
    global DORAKUE
    x_list = [pos[v][0]-width, pos[v][0], pos[v][0]+width]
    y_list = [pos[v][1]-height, pos[v][1], pos[v][1]+height]

    best_pos = [pos[v][0], pos[v][1]]
    _dist = float("inf")

    for x in x_list:
        for y in y_list:
            ax = pos[u][0] - x
            ay = pos[u][1] - y
            adist = (ax ** 2 + ay ** 2) ** 0.5
            if use_ideal:
               if abs(_dist-ideal_dist) > abs(adist-ideal_dist):
                    best_pos[0] = ax
                    best_pos[1] = ay
                    _dist = adist
            else:
                if _dist > adist:
                    best_pos[0] = ax
                    best_pos[1] = ay
                    _dist = adist

                   

    is_wrap = not(best_pos[0] == pos[v][0] and best_pos[1] == pos[v][1])
    if is_wrap:
        DORAKUE = True

    return _dist, best_pos, is_wrap


def dist_around_position(pos, u, v, width, height, ideal_dist, use_ideal=False):
    _dist, best_pos, is_wrap = dist_around9(
        pos, u, v, width, height, ideal_dist, use_ideal)
    return best_pos


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
        # TODO:ここも9箇所にしないといけない
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
            norm = dist_around(pos, i, j, width, height, l[i][j])
            # norm = math.sqrt((_pos[i][0]-_pos[j][0]) **
            #                  2 + (_pos[i][1]-_pos[j][1])**2)
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
