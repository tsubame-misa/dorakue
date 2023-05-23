import json
from networkx.readwrite import json_graph
from common import log, drawGraph
import setup
from algorithm import torusCenter, torusBfs, kameKame


filename = './graph/les_miserables.json'
graph = json_graph.node_link_graph(json.load(open(filename)))

len_list = [500, 800, 1000]
all_log = {"file": filename}

great = {l: [] for l in len_list}
good = {l: [] for l in len_list}
for _len in len_list:
    width = _len
    height = _len
    wh_log = {}
    print(_len)
    for i in range(10):
        setup.init()
        setup.set_roop1(100)

        time = setup.get_time()
        center = torusCenter.torus_center(graph, width, height)
        bfs = torusBfs.torus_bfs(graph, width, height)
        kame = kameKame.kamada_kawai(graph, width, height)

        drawGraph.create_compare_fig()

        _log = log.get_log()
        wh_log[str(time)] = _log

        l = str(kame).split(".")
        keta = 10**(len(l[0]))
        keta_1 = 10**(len(l[0])-1)

        # ドラクエのログは同じなので片方だけ見ればいい
        message = str(time)
        if center <= keta:
            message += " 同じ桁数"
            great[_len].append(str(time))
        elif abs(kame-center) <= keta_1:
            message += " 誤差"+keta_1+"以内"
            great[_len].append(str(time))
        print(message)

    all_log[str(_len)] = wh_log

log.clear()
time = setup.get_time()
log.create_log(all_log)

print(great)
print(good)
