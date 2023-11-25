from PyPDF2 import PdfReader
from tkinter.filedialog import askopenfilename
import pandas as pd

file = PdfReader(askopenfilename())
suborders = []
for i in range(file.numPages):
    extraction = file.getPage(i).extractText().split()
    for j in extraction:
        if '_' in j:
            suborders.append(j)

suborders_without_gibbresh = []
for i in suborders:
    x = i.split('_')
    suborders_without_gibbresh.append(x[0] + '_' + x[1][0])

pd.Series(suborders_without_gibbresh).to_excel('ans.xlsx')