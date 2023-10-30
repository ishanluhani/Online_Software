# Importing the module
from moviepy.editor import *
import os

# def use(path):
#
#     # uploading the video we want to edit
#     try:
#         VideoFileClip('/'.join(path.split('/')[:-1]) + '/output.mp4')
#         return '/'.join(path.split('/')[:-1]) + '/output.mp4'
#     except:
#         a = path
#         video = VideoFileClip(a)
#
#         # getting width and height of video 1
#         width_of_video1 = video.w
#         height_of_video1 = video.h
#
#         print("Width and Height of original video : ", end = " ")
#         print(str(width_of_video1) + " x ", str(height_of_video1))
#
#         print("#################################")
#
#         # compressing
#         if width_of_video1 >= 650:
#             video_resized = video.resize(.5)
#         else:
#             video_resized = video.resize(1)
#
#         # getting width and height of video 2 which is resized
#         width_of_video2 = video_resized.w
#         height_of_video2 = video_resized.h
#
#         print("Width and Height of resized video : ", end = " ")
#         print(str(width_of_video2) + " x ", str(width_of_video2))
#
#         print("###################################")
#
#
#         # displaying final clip
#         video_resized.write_videofile('/'.join(path.split('/')[:-1]) + '/output.mp4', codec='libx264')
#         # os.remove(path)
#         # path_copy = path.split('.')[0]
#         # path_copy += ' cropped.mp4'
#         # path = path.replace('\\', '/')
#         # path_copy = path_copy.replace('\\', '/')
#         # os.rename('/'.join(path.split('/')[:-1]) + '/output.mp4')
#         # return path_copy


def use(path):
    out_path = '/'.join(path.split('/')[:-1]) + '/output.mp4'
    if not os.path.isfile(out_path):
        # os.system(f'ffmpeg -i "{path}" -c:a copy -x265-params crf=30 "{out_path}"')
        os.system(f'ffmpeg -i "{path}" -vcodec libx265 -crf 25 "{out_path}"')
    return out_path

if __name__ == '__main__':
    use('//RASPBERRYPI/128gbSSD/returns ex/Group 1/VID_20230721_144742 - Copy - Copy.mp4')