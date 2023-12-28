import file_grouper
import os
import pandas as pd
from PIL import Image
from video_compress_two import compress_video
import img_to_text_main_groups_version
import choose_type_of_ticket
import upload_file

data, old_path = file_grouper.ask_and_group()
group_data = {}
print(data, old_path)

# Getting group numbers and names from the selected group
group_names = pd.Series(list(os.walk(old_path))[0][1])
group_names = group_names.apply(lambda x: os.path.join(old_path, x)).to_list()

print(group_names)

# Iterate through various groups and extract the photos and video to be compressed
for group in group_names:
    group_name = group.split('/')[-1]
    each_group_data = pd.Series(list(os.walk(group))[0][2])
    each_group_data = list(each_group_data.apply(lambda x: os.path.join(group, x)))
    group_data[group_name] = each_group_data
    print(each_group_data)

    # separating the files into videos and images to compress them
    for file in each_group_data:
        if file.endswith('mp4'):
            out_file_path = os.path.join(group, 'output.mp4')
            if not os.path.exists(out_file_path):
                compress_video(file,
                               out_file_path, 20 * 1000)
        else:
            image = Image.open(file)
            image = image.resize((1800, 1350))  # width, height
            image.save(file)

# Using the data of compressed photos and videos to group them by product img, packet id img, waybill img and video
print(group_data, 'ryh')
img_to_text_main_groups_version.calibrate(group_data)
classes_data = img_to_text_main_groups_version.data
print(classes_data)

# Modifying the old video path to the new compressed video path
for group in classes_data:
    group_data = classes_data[group][1]['video'][0]
    video_output = os.path.join(group_data.split('\\')[0], 'output.mp4')
    classes_data[group][1]['video'] = [video_output]

print(classes_data)
a, description = choose_type_of_ticket.run('I have received wrong return', classes_data['Group 1'][1])
data = description.to_dict()
description = list(data['description'].values())[0]
link = list(data['link'].values())[0]
print(description)
upload_file.run_file(classes_data['Group 1'], description, link)