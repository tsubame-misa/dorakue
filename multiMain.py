import json
from networkx.readwrite import json_graph
from dorakue import dorakue_choice_center
from dorakue_bfs import dorakue_bfs
from kameKame import kamada_kawai
import common
import commonLog
import commonDrawGraph


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
        common.init()
        time = common.get_time()
        center = dorakue_choice_center(graph, width, height)
        bfs = dorakue_bfs(graph, width, height)
        kame = kamada_kawai(graph, width, height)

        commonDrawGraph.create_compare_fig()

        log = commonLog.get_log()
        wh_log[str(time)] = log

        l = str(kame).split(".")
        keta = 10**(len(l[0]))
        keta_1 = 100*(len(l[0])-1)

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

commonLog.clear()
time = common.get_time()
commonLog.create_log(all_log)

print(great)
print(good)
