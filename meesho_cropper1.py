import PyPDF2
import datetime
import fitz
import tkinter.filedialog
import pandas
import fpdf
import os, glob


sizes = ['S', 'M', "L", 'XL', 'XXL', 'XXXL', '4XL']


def shrink(in_file):
    with open(in_file, 'rb') as infp:
        reader = PyPDF2.PdfFileReader(infp)
        writer = PyPDF2.PdfFileWriter()
        sku_to_page_ratio = []
        for i in range(reader.numPages):
            page = reader.getPage(i)
            page_es = page.extractText()
            if '_' in page_es:
                page_es = page_es.split()
                page.mediaBox.lowerLeft = [0, 450]
                writer.addPage(page)
        in_file = in_file.replace('\\', '/')
        f = fr'D:/ONLINE Data/Suborder Labels/{datetime.datetime.now().day}.{datetime.datetime.now().month}.{datetime.datetime.now().year} {in_file.split(r"/")[-1]}'
        with open(f, 'wb') as outfp:
            writer.write(outfp)
            return f


def get_data(in_file):
    reader = fitz.open(in_file)
    sub_order = []
    awbs = []
    address = []
    sku_to_page_ratio = []
    ans = pandas.DataFrame(columns=['Suborders', ' ', 'AWB', '   ', 'Address'])
    page_num = 0
    for i in reader:
        caught_awb = False
        page_num += 1
        pages = i.get_text()
        page = pages.split()
        print(page)
        if 'Fold' in page:
            sub_order.append(page[page.index('Fold')-1])
        if 'Product' in page and not page[page.index('Product')-1].startswith('MSS'):
            awbs.append(page[page.index('Product')-1])
            caught_awb = True
        if 'Address' in page:
            address.append(' '.join(page[page.index('Address')+1:page.index('undelivered,')-2]))
        else:
            address.append(''.join(page[:page.index('From:')]))
        skus = []
        if 'Fold' in page:
            a = page[page.index('Order') + 2: page.index('Fold')]
            x = 0
            while a[x-1] not in sizes:
                skus.insert(0, ' ')
                skus.insert(0, a[x])
                x+=1
                if x == len(a):
                    break
            try: skus.append(a[x])
            except: skus.append('1')
        sub_orders = 0
        for x in page:
            if not caught_awb and x.startswith('ER'):
                caught_awb = True
                awbs.append(x)
            if '_' in x and x[-1].isdigit() and len(x) > 8:
                sub_orders += 1
        if not caught_awb:
            awbs.append('')

        sku_to_page_ratio.append([page_num, ''.join(skus)])

    sku_to_page_ratio.sort(key=lambda x: x[1])
    skuize_data(sku_to_page_ratio, in_file)
    ans['Suborders'] = pandas.Series(sub_order)
    ans['AWB'] = pandas.Series(awbs)
    ans['Address'] = pandas.Series(address)
    ans.to_excel(rf'D:\ONLINE Data\Meesho Customer DataBase\{in_file.split("/")[-1][:-4]}.xlsx', index=False)


def skuize_data(data, name):
    # data = [15, 'MSGSHCH1-ROYAL-BLU1', 1] [page Number, size+sku, quantity]

    reader = PyPDF2.PdfFileReader(name)
    writer = PyPDF2.PdfFileWriter()
    line_writer = fpdf.FPDF()
    data.sort(key=lambda x: x[1].upper())
    filtered_data = []
    last = 'hi'  # hi has no meaning, it is just to separate it from empty
    last_size = 'hi' # it is to get last size to add double lines
    for i in data:
        line_writer.add_page()
        print(data, i)
        if i[1]:
            if last_size != i[1].split()[0]:
                filtered_data.append('-----/------')
                line_writer.rect(206, 0, 1, 150, style='F')
                line_writer.rect(208, 0, 1, 150, style='F')
            else:
                if last != i[1]:
                    filtered_data.append('-----')
                    line_writer.rect(206, 0, 1, 150, style='F')
            if i[1] and i[1][-1] != '1':
                filtered_data.append('||||||')
                line_writer.rect(0, 120, 210, 2, style='F')
            filtered_data.append(i)
            last = i[1]
            last_size = last.split()[0]
        writer.add_page(reader.getPage(i[0] - 1))
    print(filtered_data)
    line_writer.output('line_data.pdf')
    line_reader = PyPDF2.PdfFileReader('line_data.pdf')
    for i in range(writer.getNumPages()):
        page = writer.getPage(i)
        page.mergePage(line_reader.getPage(i))
    # for index, page in enumerate(data):
    with open(name, 'wb') as wb:
        writer.write(wb)
        # os.startfile(name, 'print')



if __name__ == '__main__':
    # in_file2 = tkinter.filedialog.askopenfilename()
    path = 'C:/Users/ishan/Downloads/'
    files = list(filter(os.path.isfile, glob.glob(path + "*")))
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    if 'Sub_Order' in files[0]:
        get_data(shrink(files[0]))
    else:
        print('Please check downloaded order file')


