import datetime
from common import calcDrawInfo, initGraph
from common import log
from common import drawGraph


DEFAULT_LOOP1 = 30
DEFAULT_LOOP2 = 10
DEFAULT_TERAM = 10
DEFAULT_DIR_NAME = "result"

LOOP1 = DEFAULT_LOOP1
LOOP2 = DEFAULT_LOOP2
SGD_LOOP = DEFAULT_LOOP1
TERM = 10
LOG_DIR_NAME = DEFAULT_DIR_NAME


def get_loop():
    return LOOP1, LOOP2


def get_SGD_loop():
    return SGD_LOOP


def get_edge_width():
    return 100


def set_roop1(value):
    global LOOP1
    LOOP1 = value


def set_roop2(value):
    global LOOP2
    LOOP2 = value


def get_time():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y%m%d%H%M%S')
    return d


def init(time=None):
    global LOOP1, LOOP2, TERM, LOG_DIR_NAME
    drawGraph.clear()
    log.clear()
    initGraph.clear()
    LOOP1 = DEFAULT_LOOP1
    LOOP2 = DEFAULT_LOOP2
    TERM = DEFAULT_TERAM
    LOG_DIR_NAME = DEFAULT_DIR_NAME

    if time == None:
        time = get_time()
    drawGraph.set_time(time)
    log.set_time(time)


def get_len():
    return [3000]


def set_term(value):
    global TERM
    TERM = value


def get_term():
    return TERM


def set_dir_name(name):
    global LOG_DIR_NAME
    LOG_DIR_NAME = name


def get_dir_name():
    return LOG_DIR_NAME
