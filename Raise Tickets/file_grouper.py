import glob
import os
import shutil
import subprocess
from tkinter.filedialog import askdirectory

group = {}


def absoluteFilePaths(directory):
    directory = directory.replace('//', '\\')
    try:
        for file in os.listdir(directory):
            file = '/'.join([directory, file])
            print(file)
            yield file
    except Exception as e:
        print(e)


def already(path):
    data = {}
    for index, i in enumerate(os.listdir(path)):
        print(os.path.join(path, i))
        data[f'Group {index+1}'] = {'paths': list(absoluteFilePaths(os.path.join(path, i)))}
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
            if id_ > -1:
                try:
                    os.mkdir(path + f'/Group {id_+1}')
                    print(path + f'/Group {id_+1}')
                    for j in make_groups:
                        print(j)
                        a = j.split('\\')[-1]
                        shutil.move(j, path + f'Group {id_+1}/{a}')
                except FileExistsError:
                    continue
            make_groups = [i]
            id_ += 1
        else:
            make_groups.append(i)
    for j in make_groups:
        print(j)
        a = j.split('\\')[-1]
        shutil.move(j, path + f'Group 1/{a}')


    group = already(path)



