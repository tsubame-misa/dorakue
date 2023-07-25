import json
import os
import setup

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


def create_log_folder():
    dir_name = setup.get_dir_name()
    path = os.getcwd()
    new_dir_path = path + "/" + dir_name

    if os.path.isdir(new_dir_path):
        return

    os.mkdir(new_dir_path)

    folders = ["log", "SGD", "torusSGD", "compare"]
    for f in folders:
        new_dir_path = path + "/" + dir_name + "/" + f
        os.mkdir(new_dir_path)


def create_log(_log=None, filename=""):
    dir_name = setup.get_dir_name()
    print(LOG)
    if _log == None:
        _log = LOG

    path = os.getcwd()
    with open(path + "/"+dir_name+"/log/" + filename + "-" + TIME + ".json", "w") as f:
        json.dump(_log, f)


def get_log():
    return LOG
