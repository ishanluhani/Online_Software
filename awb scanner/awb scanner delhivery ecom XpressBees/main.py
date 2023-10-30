import numpy
import PyPDF2
import pygame.mixer
pygame.mixer.init()
pass_sound = pygame.mixer.Sound('beep-06.mp3')
error_sound = pygame.mixer.Sound('beep-03.mp3')
repeat_sound = pygame.mixer.Sound('censor-beep-01.mp3')
def load_last():
    global bees_data, delhi_data, ecom_data, run_data
    data = numpy.load('youcantseeit.npy')
    delhi_data = list(data[0])
    ecom_data = list(data[1])
    bees_data = list(data[2])
    bees_data = list(data[3])
def create_dataframe2(path, id2, c):
    pdf = PyPDF2.PdfFileReader(open(path, 'rb'))
    page_text_formatted = []
    cour = []
    all_awbs = []
    for i in range(pdf.numPages):
        page_text_ = pdf.getPage(i).extractText().split()
        if page_text_[0] != 'Picklist':
            page_text = pdf.getPage(i).extractText()[pdf.getPage(i).extractText().index(')')+1:].split()
            page_text_formatted.append(page_text)
            t = pdf.getPage(i).extractText()
            cour.append(t[t.find('Courier : ')+len('Courier : '):t.find('Supplier')])
            all_awbs.append(page_text)
    return all_awbs, cour, page_text_formatted


import tkinter.filedialog
from tkinter import *
text2 = 0

def reset():
    global text2
    text2 = 0

def load(cour):
    global ecom_data, delhi_data, bees_data, text2, run_data
    text2 = 0
    root = Tk()
    text_area = Entry(root, width=100)

    label = Label(root)
    label1 = Label(root, text=f'Scanned: {text2}')
    Button(root, text='reset', command=reset).grid(row=0, column=0)
    text = ''
    last_text2 = 0
    c = 0
    c1 = 0
    listbox = Listbox(root, height=38, width=50, bg='black', fg='white')
    listbox1 = Listbox(root, height=38, width=50, bg='black', fg='white')
    cont = 0
    j = []

    for i in file_order:
        if couriur[file_order.index(i)][0] == cour[0]:
            for x in i:
                j.append(x)
    for i in file_order:
        if couriur[file_order.index(i)][0] == cour[0]:
            for a, x in enumerate(i):
                cont += 1
                if cour.startswith('X'):
                    if x[:4] == '1340' and len(x) > len('13403334959_'):
                        if bees_data[j.index(x)]:
                            listbox.insert(END, f'{cont}   {x}   {bees_data[j.index(x)]}')
                            text2 += 1
                        else:
                            listbox1.insert(END, f'{cont}   {x}   {bees_data[j.index(x)]}')
                    else:
                        cont -= 1
                if cour.startswith('Ec'):
                    n = len(x)
                    if n < 11 and n > len('9734749027')-3:
                        if ecom_data[j.index(x)]:
                            listbox.insert(END, f'{cont}   {x}   {ecom_data[j.index(x)]}')
                            text2 += 1
                        else:
                            listbox1.insert(END, f'{cont}   {x}   {ecom_data[j.index(x)]}')
                    else:
                        cont -= 1
                if cour.startswith('D'):
                    if x[:4] == '1490':
                        if delhi_data[j.index(x)]:
                            listbox.insert(END, f'{cont}   {x}   {delhi_data[j.index(x)]}')
                            text2 += 1
                        else:
                            listbox1.insert(END, f'{cont}   {x}   {delhi_data[j.index(x)]}')
                    else:
                        cont -= 1
                if cour.startswith('El'):
                    if x[0] == 'E':
                        if run_data[j.index(x)]:
                            listbox.insert(END, f'{cont}   {x+i[a+1]}   {run_data[j.index(x)]}')
                            text2 += 1
                        else:
                            listbox1.insert(END, f'{cont}   {x+i[a+1]}   {run_data[j.index(x)]}')
                    else:
                        cont -= 1

                listbox.insert(END, '--------------------------------')
    Label(root, text=f'total count: {cont}').grid(row=1, column=0)
    text_area.grid(row=2, column=0)
    label.grid(row=3, column=0)
    label1.grid(row=4, column=0)
    listbox.grid(row=5, column=0)
    listbox1.grid(row=5, column=1)
    # print(len(x), x, len(j), i)
    done = []
    start_c1_counter = False
    while True:
        if text_area.get() != '':
            alls = []
            number = text_area.get()
            for i in file_order:
                try:
                    if cour.startswith('X'):
                        bees_data[j.index(number)] = 'done'
                    elif cour.startswith('Ec'):
                        ecom_data[j.index(number)] = 'done'
                    elif cour.startswith('El'):
                        run_data[j.index(number)] = 'done'
                    elif cour.startswith('D'):
                        delhi_data[j.index(number)] = 'done'
                except ValueError as e:
                    continue
                if number[:-2] in i and couriur[file_order.index(i)] == cour:
                    if not number in done:
                        text2 += 1
                        text = 'Pass'
                        numpy.save('youcantseeit.npy', numpy.array([delhi_data, ecom_data, bees_data, run_data]))
                    else:
                        if last_text2+1 != text2:
                            text = 'REPEAT'
                    done.append(number)
                alls.append(number in i and couriur[file_order.index(i)] == cour)

            if not any(alls):
                text = 'Error'
            c += 1
            if c >= 1000:
                if text == 'Pass':
                    pass_sound.play()
                elif text == 'REPEAT':
                    repeat_sound.play()
                else:
                    error_sound.play()
                text_area.delete(0, END)
                start_c1_counter = True
                last_text2 = text2
                c = 0

        if start_c1_counter:
            c1 += 1
            if label['text'] == 'Pass':
                label['fg'] = 'green'
            else:
                label['fg'] = 'red'
            label['text'] = text
            if c1 >= 5000:
                start_c1_counter = False
                c1 = 0
        else:
            label['text'] = ''
        label1['text'] = f'Scanned: {text2}'
        root.update()
from tkinter import *
file_order, couriur, page_text = create_dataframe2(tkinter.filedialog.askopenfilename(), '', '')
root = Tk()
length = 0
for i in file_order: length += len(i)
delhi_data = ['']*length
bees_data = ['']*length
ecom_data = ['']*length
run_data = ['']*length
Button(root, text='Delhivery', command=lambda: load('Delhivery ')).grid(row=0, column=0)
Button(root, text='Ecom Express', command=lambda: load('Ecom Express ')).grid(row=1, column=0)
Button(root, text='Xpress Bees', command=lambda: load('Xpress Bees ')).grid(row=2, column=0)
Button(root, text='ElasticRun', command=lambda: load('ElasticRun')).grid(row=3, column=0)
Button(root, text='load', command=lambda: load_last()).grid(row=4, column=0)
root.mainloop()
