import datetime
from common import calcDrawInfo
from common import log
from common import drawGraph


DEFAULT_LOOP1 = 50
DEFAULT_LOOP2 = 20
TERM_DEFAULT = 10

LOOP1 = DEFAULT_LOOP1
LOOP2 = DEFAULT_LOOP2
TERM = TERM_DEFAULT


def get_loop():
    return LOOP1, LOOP2


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
    global LOOP1, LOOP2
    drawGraph.clear()
    log.clear()
    calcDrawInfo.clear()
    LOOP1 = DEFAULT_LOOP1
    LOOP2 = DEFAULT_LOOP2
    TERM = DEFAULT_LOOP1

    if time == None:
        time = get_time()
    drawGraph.set_time(time)
    log.set_time(time)


def get_len():
    return [500, 750, 1000]


def set_term(value):
    global TERM
    TERM = value


def get_term():
    return TERM
