from tkinter.filedialog import askdirectory
import os, glob, time
import pandas as pd
from PyPDF2 import PdfReader


output_folder = 'C:/Users/ishan/Downloads'
files = list(filter(os.path.isfile, glob.glob(askdirectory() + "/*")))
# example = time.gmtime(os.path.getmtime(files[0]))
# print(example.tm_mday, example.tm_mon, example.tm_year, sep='-')
files = list(map(lambda x: [x, time.gmtime(os.path.getmtime(x))], files))
OUT_PASS = {}
files.sort(key=lambda x: x[1], reverse=True)
courier_data = {'ECOM EXPRESS'.upper(): [], '': [], ' ': [], 'XPRESS BEES'.upper(): [], '  ': [], '   ': [], 'DELHIVERY'.upper(): [],
                '    ': [], '     ': [], 'SHADOWFAX'.upper(): [], '      ': [], '       ': [], 'VALMO'.upper(): [], '        ': [],
                '         ': [], 'DTDC': []}

last_out_file_path = ''
for file, date in files:
    courier_decided = ''
    time_uploaded = f'{date.tm_mday}-{date.tm_mon}-{date.tm_year}'
    output_file_path = os.path.join(output_folder, f'{time_uploaded} manual file.xlsx')
    if last_out_file_path != output_file_path:
        courier_data = {'ECOM EXPRESS'.upper(): [], '': [], ' ': [], 'XPRESS BEES'.upper(): [], '  ': [], '   ': [],
                        'DELHIVERY'.upper(): [],
                        '    ': [], '     ': [], 'SHADOWFAX'.upper(): [], '      ': [], '       ': [],
                        'VALMO'.upper(): [], '        ': [],
                        '         ': [], 'DTDC': []}
    if not os.path.exists(output_file_path):
        df = pd.DataFrame().to_excel(output_file_path, index=False)
        OUT_PASS[output_file_path] = True

    pdf = PdfReader(file)
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        page_extracted_text = page.extract_text()
        print(page_extracted_text)

        if 'Ecom Express' in page_extracted_text and not courier_decided:
            courier_decided = 'ECOM EXPRESS'
        elif 'SR Name' in page_extracted_text and not courier_decided:
            courier_decided = 'XPRESS BEES'
        elif 'Dispatch ID' in page_extracted_text and not courier_decided:
            courier_decided = 'DELHIVERY'
        elif 'Rider Name' in page_extracted_text and not courier_decided:
            courier_decided = 'SHADOWFAX'

        if courier_decided:
            page_extracted_text = page_extracted_text.split()
            print(page_extracted_text)
            last_word = ''
            for index, word in enumerate(page_extracted_text):
                to_include = False
                if '_' in word:
                    word_og = word
                    word = word.split('_')
                    word = word[0] + '_' + word[1][0]

                    if courier_decided == 'ECOM EXPRESS':
                        to_include = page_extracted_text[index+2] == 'Delivered'
                        if to_include:
                            courier_data[courier_decided].append(word)
                    if courier_decided == 'SHADOWFAX':
                        courier_data[courier_decided].append(page_extracted_text[index - 2])
                if word == 'RTO' or word == 'DTO' and courier_decided == 'DELHIVERY':
                    to_include = 'ACCEPTED' in page_extracted_text[page_extracted_text.index(word) + 1]
                    print(to_include, 'yoo', page_extracted_text[page_extracted_text.index(word) + 1])
                    if to_include:
                        courier_data[courier_decided].append(last_word)
                if word == 'MPS' and courier_decided == 'XPRESS BEES':
                    courier_data[courier_decided].append(page_extracted_text[index - 1])
                last_word = word

    courier_data_final = {}
    for courier in courier_data:
        courier_data_final[courier] = pd.Series(courier_data[courier])
    out_data = pd.DataFrame(courier_data_final)
    print(out_data, 'kk', output_file_path)
    if not os.path.isfile(output_file_path) or OUT_PASS.get(output_file_path):
        print('pass')
        OUT_PASS[output_file_path] = True
        out_data.to_excel(output_file_path, index=False)

    last_out_file_path = output_file_path
