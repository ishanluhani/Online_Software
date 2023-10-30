from PyPDF2 import PdfFileReader, PdfFileWriter
from tkinter.filedialog import askopenfilename

big_pdf = PdfFileReader(askopenfilename())
small_pdf = PdfFileReader(askopenfilename())
small_pages = [i.extractText() for i in small_pdf.pages]
output_file = PdfFileWriter()

for i in range(big_pdf.numPages):
    a = big_pdf.getPage(i)
    if not a.extractText() in small_pages:
        output_file.addPage(a)

output_file.write('pdf_file.pdf')