import file_grouper
import os
import pandas as pd
from PIL import Image

data, old_path = file_grouper.ask_and_group()
print(data, old_path)

# Getting group numbers and names from the selected group
group_names = pd.Series(list(os.walk(old_path))[0][1])
group_names = group_names.apply(lambda x: os.path.join(old_path, x)).to_list()

print(group_names)

# Iterate through various groups and get the photos and video to be compressed
for group in group_names:
    each_group_data = pd.Series(list(os.walk(group))[0][2])
    each_group_data = list(each_group_data.apply(lambda x: os.path.join(group, x)))
    print(each_group_data)

    # separating the files into videos and images to compress them
    for file in each_group_data:
        if not file.endswith('mp4'):
            image = Image.open(file)
            image = image.resize((1800, 1350))  # width, height
            image.save(file)

