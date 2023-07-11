import json
import os

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


def create_file(time):
    dir = os.getcwd()
    path = "/result/log/" + time + ".json"
    f = open(path, "w")
    f.write()
    f.close()


def create_log(_log=None):
    print(LOG)
    if _log == None:
        _log = LOG

    path = os.getcwd()
    with open(path + "/result/log/" + TIME + ".json", "w") as f:
        json.dump(_log, f)


def get_log():
    return LOG
