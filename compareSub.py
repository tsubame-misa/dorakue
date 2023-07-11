import json


# json.load関数を使ったjsonファイルの読み込み
with open('./result/log/20230607161837.json') as f:
    data = json.load(f)

len_list = [500, 750,   1000]
# len_list = [1000000]
score_result = []

for _len in len_list:
    dist_score = 0
    delta_score = 0
    for date, result in data[str(_len)].items():

        # delta_torus_best_sd = result["torus_kame"]["delta"]["sd"]
        # # delta_torus_best_sd_key = ""
        # delta_kamada_kawai_sd = result["kamada_kawai"]["delta"]["sd"]

        # dist_torus_best_sd = result["torus_kame"]["dist"]["sd"]
        # # dist_torus_best_sd_key = ""
        # dist_kamada_kawai_sd = result["kamada_kawai"]["dist"]["sd"]

        delta_torus_best_sd = result["torusSGD"]["delta"]["sd"]
        # delta_torus_best_sd_key = ""
        delta_kamada_kawai_sd = result["SGD"]["delta"]["sd"]

        dist_torus_best_sd = result["torusSGD"]["dist"]["sd"]
        # dist_torus_best_sd_key = ""
        dist_kamada_kawai_sd = result["SGD"]["dist"]["sd"]

        # for key in result:
        #     print(key)
        #     if dist_torus_best_sd > result[key]["dist"]["sd"]:
        #         dist_torus_best_sd = result[key]["dist"]["sd"]
        #         dist_torus_best_sd_key = key
        #     if delta_torus_best_sd > result[key]["delta"]["sd"]:
        #         delta_torus_best_sd = result[key]["delta"]["sd"]
        #         delta_torus_best_sd_key = key

        # print(dist_kamada_kawai_sd, dist_torus_best_sd)

        if dist_torus_best_sd < dist_kamada_kawai_sd:
            # print("dist", dist_torus_best_sd_key, date,
            #       dist_torus_best_sd, dist_kamada_kawai_sd)
            dist_score += 1
        if delta_torus_best_sd < delta_kamada_kawai_sd:
            # print("delta", delta_torus_best_sd_key, date,
            #       delta_torus_best_sd, delta_kamada_kawai_sd)
            delta_score += 1
        # print(date)
        # print("dist", dist_kamada_kawai_sd - dist_torus_best_sd)
        # print("delta", delta_kamada_kawai_sd - delta_torus_best_sd)
        # print()

        # print(score, delta_torus_best_sd, delta_kamada_kawai_sd)
        # print()
    print(_len, "dist", dist_score, dist_score /
          (len(data[str(_len)])), len(data[str(_len)]))
    print(_len, "delta", delta_score, delta_score /
          (len(data[str(_len)])), len(data[str(_len)]))
    print("----------------")
