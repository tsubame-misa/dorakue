import glob
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent) + "/")

from common import log
import glob
import json
import re
import setup

args = sys.argv

files30 = glob.glob(args[1] + "/*")
files20 = glob.glob(args[2] + "/*")
dir_name = args[3]

data_dict = {}

for file in files30:
    print(file)
    with open(file) as f:
        data = json.load(f)
        file_name = re.split("[/-]", file)[-3]
        data_dict[file_name] = data

print(data_dict.keys())

for file in files20:
    with open(file) as f:
        data = json.load(f)
        file_name = re.split("[/-]", file)[-3]
        merged_data = data + data_dict[file_name]
        data_dict[file_name] = merged_data

setup.set_dir_name(dir_name)
log.create_log_folder()
for name in data_dict.keys():
    log.create_log(data_dict[name], name + "-all")
