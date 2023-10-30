# hihihihihihihi

# import PyPDF2
#
# def extract(in_file, out_file):
#     with open(in_file, 'rb') as infp:
#         reader = PyPDF2.PdfFileReader(infp)
#         page = reader.getPage(0)
#         pagecop = reader.getPage(0)
#         writer = PyPDF2.PdfFileWriter()
#         print(page.mediaBox)
#         page.rotateClockwise(90)
#         page.mediaBox.upperRight = [600,430]
#         writer.addPage(page)
#         pagecop.mediaBox.lowerLeft = [0,430]
#         pagecop.mediaBox.upperRight = [600,842]
#         writer.addPage(pagecop)d
#         # you could do the same for page.trimBox and page.cropBox
#         with open(out_file, 'wb') as outfp:
#             writer.write(outfp)

#
# import tkinter.filedialog
# if __name__ == '__main__':
#     in_file = tkinter.filedialog.askopenfilename()
#     out_file = 'hello.pdf'
#
#     extract(in_file, out_file)

import PyPDF2
import datetime
import os, glob


def shrink(in_file):
    with open(in_file, 'rb') as infp:
        reader = PyPDF2.PdfFileReader(infp)
        writer = PyPDF2.PdfFileWriter()
        sub_orders = []
        for i in range(reader.numPages):
            page = reader.getPage(i)
            page.mediaBox.lowerLeft = [185, 460]
            page.mediaBox.top = 815
            page.mediaBox.right = 405
            print(page.mediaBox.right)
            writer.addPage(page)
        in_file = in_file.replace('\\', '/')
        f = fr'D:/ONLINE Data/Suborder Labels/{datetime.datetime.now().day}.{datetime.datetime.now().month}.{datetime.datetime.now().year} {in_file.split(r"/")[-1]}'
        with open(f, 'wb') as outfp:
            writer.write(outfp)
            # os.startfile(f, 'print')
            return f

if __name__ == '__main__':
    path = 'C:/Users/ishan/Downloads/'
    files = list(filter(os.path.isfile, glob.glob(path + "*")))
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    if 'Flipkart' in files[0]:
        shrink(files[0])
    else:
        print('Please check downloaded order file')


