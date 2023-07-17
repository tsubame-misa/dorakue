import json
import pandas as pd

tmp = {"edge_length_variance": 0,
       "minimum_angle": 0,
       "edge_crossings": 0,
       "dist_variance": 0,
       "dist_mean": 0,
       "delta_variance": 0,
       "delta_mean": 0,
       "count": 0}

# json.load関数を使ったjsonファイルの読み込み
with open('./result/log/bull-20230712153545.json') as f:
    data = json.load(f)

len_array = [_len for _len in data.keys()][1:]
alg_array = ["SGD", "torusSGD", "kamada_kawai", "torus_kame"]

result = dict()

for _len in data.keys():
    alg_sum_result = {}
    if _len == "file":
        continue
    for time in data[_len].keys():
        for alg in data[_len][time].keys():
            # 回り込みがなかった場合は集計しない
            if alg == "torusSGD" or alg == "torus_kame":
                if not data[_len][time][alg]["wrap"]:
                    continue
            if not alg in alg_sum_result:
                alg_sum_result[alg] = tmp.copy()
            alg_sum_result[alg]["edge_length_variance"] += data[_len][time][alg]["edge_length_variance"]
            alg_sum_result[alg]["minimum_angle"] += data[_len][time][alg]["minimum_angle"]
            alg_sum_result[alg]["edge_crossings"] += data[_len][time][alg]["edge_crossings"]
            alg_sum_result[alg]["dist_variance"] += data[_len][time][alg]["dist"]["sd"]
            alg_sum_result[alg]["dist_mean"] += data[_len][time][alg]["dist"]["mean"]
            alg_sum_result[alg]["delta_variance"] += data[_len][time][alg]["delta"]["sd"]
            alg_sum_result[alg]["delta_mean"] += data[_len][time][alg]["delta"]["mean"]
            alg_sum_result[alg]["count"] += 1
    alg_mean_result = {}
    for alg in alg_sum_result.keys():
        alg_mean_result[alg] = {}
        count = alg_sum_result[alg]["count"]
        alg_mean_result[alg]["count"] = count
        for item in alg_sum_result[alg].keys():
            if item == "count":
                continue
            alg_mean_result[alg][item] = alg_sum_result[alg][item]/count
    result[_len] = alg_mean_result

for _len in result.keys():
    print(_len)
    df = pd.DataFrame.from_dict(result[_len])
    print(df)
    print("---------------------------------")


# print(result)
