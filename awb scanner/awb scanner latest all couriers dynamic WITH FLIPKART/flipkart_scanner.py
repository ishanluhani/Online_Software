# importing required modules
from tkinter import *
from tkinter.filedialog import askopenfilename
import fitz
import pygame.mixer

pygame.mixer.init()

def run():
    pass_sound = pygame.mixer.Sound('beep-06.mp3')
    repeat_sound = pygame.mixer.Sound('censor-beep-01.mp3')
    error_sound = pygame.mixer.Sound('beep-03.mp3')
    doc = fitz.open(askopenfilename())
    text = ""
    for page in doc:
        text+=page.get_text()


    words = text.split('\n')
    awbs = []
    last = ''
    for i in words:
        if i.startswith('OD'):
            print(last)
            awbs.append(last)
        last = i

    print(awbs)
    awb_copy = awbs.copy()
    awbs_scanned = []

    root = Tk()
    root.geometry('605x586')
    text_area = Entry(root, width=50)
    text_area.place(x=0, y=0)
    listbox = Listbox(root, height=34, width=50, bg='black', fg='white')
    listbox.place(x=0, y=40)
    listbox1 = Listbox(root, height=34, width=50, bg='black', fg='white')
    listbox1.place(x=302, y=40)
    check_text = Label(root, text='')
    check_text.place(x=315, y=0)
    left = len(awbs_scanned)
    right = len(awb_copy)
    info_count_text = Label(root, text=f'Total Count: {len(awbs)}')
    info_count_text.place(x=360, y=0)
    left_label = Label(root, text=f'Left: {left}')
    left_label.place(x=130, y=20)
    right_label = Label(root, text=f'Right: {right}')
    right_label.place(x=415, y=19)
    # print(info_text['text'].split())
    timer = 0
    for index, number in enumerate(awb_copy):
        listbox1.insert(END, f'{index+1} {number}')
    for number in awbs_scanned:
        listbox.insert(END, number[0])

    while True:
        if text_area.get() != '':
            timer += 1
            if timer == 6000:
                timer = 0
                number = text_area.get()
                if number in awb_copy:
                    awbs_scanned.append(number)
                    listbox1.delete(awb_copy.index(number))
                    listbox.insert(END, number)
                    awb_copy.remove(number)
                    right -= 1
                    left += 1
                    left_label['text'] = f'Left: {left}'
                    right_label['text'] = f'Right: {right}'
                    check_text['text'] = 'PASS'
                    check_text['fg'] = 'green'
                    pass_sound.play()
                elif number in awbs_scanned:
                    check_text['text'] = 'REPEAT'
                    check_text['fg'] = 'blue'
                    repeat_sound.play()
                else:
                    check_text['text'] = 'ERROR'
                    check_text['fg'] = 'red'
                    error_sound.play()
                text_area.delete(0, END)
                temp_lst = []

        root.update()