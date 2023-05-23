
import os
import glob

path_list = []

files = glob.glob("./result/*")
for file in files:
    path_list.append(file)

print(files)

for dir in path_list:
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
