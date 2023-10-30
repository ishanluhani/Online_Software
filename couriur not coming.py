from camelot import read_pdf
from tkinter.filedialog import askopenfilename
import pyautogui
import time

pdf = read_pdf(askopenfilename(), pages=input('Enter pages: '))
pdf = [i.df[1][1:].str.replace('\n', '').tolist() for i in pdf]
order = []
print(pdf)
time.sleep(5)
for i in pdf:
    for j in i:
        pyautogui.typewrite(f'{j},')
        print(j)
        time.sleep(3)
print(sum([len(i) for i in pdf]))

