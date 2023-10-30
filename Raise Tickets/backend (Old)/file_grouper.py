from tkinter.filedialog import askdirectory
import os
import shutil
import glob

group = {}


def already(path):
    data = {}
    for index, i in enumerate(os.listdir(path)):
        data[f'Group {index+1}'] = {'paths': ['/'.join(path.split('/')[:-2]) + '/' + i + '/' + x for x in os.listdir(path + i)]}
    return data


def ask_and_group():
    global group

    make_groups = []
    id_ = 0
    path = askdirectory() + '/'
    files = list(filter(os.path.isfile, glob.glob(path + "*")))
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    for i in files:
        format_ = i.split('.')[-1]
        if format_ == 'mp4':
            if id_ > 0:
                os.mkdir(path + f'/Group {id_}')
                print(path + f'/Group {id_}')
                for j in make_groups:
                    print(j)
                    a = j.split('\\')[-1]
                    shutil.copy(j, path + f'Group {id_}/{a}')
            make_groups = [i]
            id_ += 1
        else:
            make_groups.append(i)

    group = already(path)

ask_and_group()
print(group)