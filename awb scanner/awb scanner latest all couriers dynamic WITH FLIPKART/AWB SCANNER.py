import joblib
from tkinter import *
from PyPDF2 import PdfFileReader
from tkinter.filedialog import askopenfilename
import pygame.mixer
import numpy
import camelot
import flipkart_scanner

pygame.mixer.init()
a = askopenfilename()
pdf = PdfFileReader(a)
awb = {}
awbs_scanned = {}
sub_orders = {}
sub_orders_scanned = {}
abc = camelot.read_pdf(a, pages='all')
abc = [i.df for i in abc]
reported_names = list(numpy.load('reported_names.npy'))
print(len(abc))
for i in range(pdf.numPages):
    text = pdf.getPage(i).extractText().split()
    if text[0] != 'Picklist':
        name = ' '.join(text[2:text.index('Supplier')])
        try:
            df_awb = abc[i][2]
            df_awb = list(filter(None, df_awb))
            df_awb = list(filter(lambda x: x != 'AWB', df_awb))
            df_awb = list(map(lambda x: ''.join(x.split('\n')), df_awb))

            df_sub = abc[i][1]
            df_sub = list(filter(None, df_sub))
            df_sub = list(filter(lambda x: x != 'Sub Order No.', df_sub))
            df_sub = list(map(lambda x: ''.join(x.split('\n')), df_sub))
            print(df_sub)

            if awb.get(name):
                awb[name].extend(df_awb)
            else:
                awb[name] = df_awb
                awbs_scanned[name] = []

            if sub_orders.get(name):
                sub_orders[name].extend(df_sub)
            else:
                sub_orders[name] = df_sub
                sub_orders_scanned[name] = []
        except:
            continue

awb_copy = awb.copy()
sub_orders_copy = sub_orders.copy()
print(sub_orders)
pass_sound = pygame.mixer.Sound('beep-06.mp3')
repeat_sound = pygame.mixer.Sound('censor-beep-01.mp3')
error_sound = pygame.mixer.Sound('beep-03.mp3')


def load():
    global awbs_scanned, awb_copy
    a = list(numpy.load('youcantseeit.npy', allow_pickle=True))
    awb_copy = a[0]
    awbs_scanned = a[1]


def scan(courier):
    global awbs_scanned, awb_copy

    secondary_root = Tk()
    secondary_root.geometry('605x586')
    text_area = Entry(secondary_root, width=50)
    text_area.place(x=0, y=0)
    listbox = Listbox(secondary_root, height=34, width=50, bg='black', fg='white')
    listbox.place(x=0, y=40)
    listbox1 = Listbox(secondary_root, height=34, width=50, bg='black', fg='white')
    listbox1.place(x=302, y=40)
    check_text = Label(secondary_root, text='')
    check_text.place(x=315, y=0)
    left = len(awbs_scanned[courier])
    right = len(awb_copy[courier])
    info_count_text = Label(secondary_root, text=f'Total Count: {len(awb[courier])}')
    info_count_text.place(x=360, y=0)
    left_label = Label(secondary_root, text=f'Left: {left}')
    left_label.place(x=130, y=20)
    right_label = Label(secondary_root, text=f'Right: {right}')
    right_label.place(x=415, y=19)
    # print(info_text['text'].split())
    timer = 0
    for index, number in enumerate(awb_copy[courier]):
        listbox1.insert(END, f'{index+1} {number}')
    for number in awbs_scanned[courier]:
        listbox.insert(END, number)
    while True:
        if text_area.get() != '':
            print(text_area.get())
            timer += 1
            if timer == 6000:
                timer = 0
                number = text_area.get()
                if number in awb_copy[courier]:
                    awbs_scanned[courier].append(number)
                    listbox1.delete(awb_copy[courier].index(number))
                    listbox.insert(END, number)
                    awb_copy[courier].remove(number)
                    right -= 1
                    left += 1
                    left_label['text'] = f'Left: {left}'
                    right_label['text'] = f'Right: {right}'
                    check_text['text'] = 'PASS'
                    check_text['fg'] = 'green'
                    pass_sound.play()
                elif number in awbs_scanned[courier]:
                    check_text['text'] = 'REPEAT'
                    check_text['fg'] = 'blue'
                    repeat_sound.play()
                else:
                    check_text['text'] = 'ERROR'
                    check_text['fg'] = 'red'
                    error_sound.play()
                text_area.delete(0, END)

        secondary_root.update()


def save():
    global awbs_scanned, awb_copy
    numpy.save('youcantseeit.npy', numpy.array([awb_copy, awbs_scanned]))

root = Tk()
buttons = []
# add couriers
Button(root, text='Delhivery', command=lambda: scan('Delhivery')).pack()
Button(root, text='Ecom Express', command=lambda: scan('Ecom Express')).pack()
Button(root, text='Valmo', command=lambda: scan('Valmo')).pack()
Button(root, text='Xpress Bees', command=lambda: scan('Xpress Bees')).pack()
Button(root, text='DTDC', command=lambda: scan('DTDC')).pack()
Button(root, text='ShadowFax', command=lambda: scan('Shadowfax')).pack()
Button(root, text='Flipkart', command=flipkart_scanner.run).pack()
Button(root, text='Save', command=save).pack()
Button(root, text='Load', command=load).pack()
root.mainloop()
