import matplotlib.pyplot as plt
import networkx as nx
import plotly.express as px
import matplotlib.pyplot as plt
import json
import common

LOG = dict()
TIME = ""


def add_log(key, value):
    LOG[key] = value


def clear():
    global LOG
    LOG = dict()


def set_time(time):
    global TIME
    TIME = time


def create_log(_log=None):
    print(_log)
    print(LOG)
    if _log == None:
        _log = LOG
    with open("./result/log/" + TIME + ".json", "w") as f:
        json.dump(_log, f)


def get_log():
    return LOG


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
