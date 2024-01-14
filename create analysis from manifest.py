from PyPDF2 import PdfReader
from tkinter.filedialog import askdirectory
import pandas as pd
import os
import json


# Defining variable that will be used Later on
sku_size_quantity_dict = {}
colors = ['Multicolor', 'Teal', 'Grey', 'Navy', 'Blue', 'White', 'Beige', 'Maroon', 'Orange', 'Brown', 'Black', 'Yellow', 'Red', 'Pink', 'NA', 'Green', 'OVERSIZE']
mapping_of_groups = {1: 'GREY-CHECK', 2: 'ROYAL-BLUE-CHECK', 3: 'WHITE-CHECK', 4: 'BROWN-CHECK', 5: 'NAVY-BLUE-CHECK',
                     6: 'RED-CHECK', 7: 'NAVY-NARROW-STRIPES', 8: 'WHITE-NARROW-STRIPES', 9: 'DARK-GREY-NARROW-STRIPES',
                     10: 'OVERSIZE-FINE-PRINT-BLACK', 11: 'OVERSIZE-FINE-PRINT-SEA-GREEN',
                     12: 'OVERSIZE-FINE-PRINT-BLUE', 13: 'OVERSIZE-FINE-PRINT-MAROON', 14: 'DUAL-LINE-CHECK-BEIGE',
                     15: "DUAL-LINE-CHECK-NAVY", 16: "DUAL-LINE-CHECK-MAROON", 17: 'ROYAL-BLUE-PLAIN',
                     18: 'PISTA-PLAIN', 19: "NAVY-PLAIN", 20: 'CEMENT-PLAIN', 21: "RUST-PLAIN", 22: "PINK-PLAIN",
                     23: "GREY-DARK-PLAIN-PRODUCT", 24: 'MAROON-PLAIN', 25: "BOTTLE-GREEN-PLAIN", 26: "SKY-PLAIN",
                     27: "BLACK-PLAIN", 28: 'WHITE-PLAIN', 29: "NAVY-BROTHERS-YELLOW", 30: "NAVY-BROTHERS-GREY",
                     31: "NAVY-BROTHERS-RED"}
folder_path = askdirectory()

for file_name in os.listdir(folder_path):
    pdf = PdfReader(os.path.join(folder_path, file_name))

    # Extracting Data of [sku, size, quantity] from picklist of the manifest
    for page_num in range(len(pdf.pages)):
        text = pdf.pages[page_num].extract_text()
        text_sep_by_space = text.split()

        # Filter the pages that have Picklist
        if text_sep_by_space[0] == 'Picklist':
            # Filtering out the table from the page
            text_sep_by_space = text_sep_by_space[text_sep_by_space.index('Quantity')+1:]

            # Removing The color column from the table
            for word in text_sep_by_space[:]:
                if word in colors:
                    text_sep_by_space.remove(word)

            # Extracting rows of table
            quantity = 0
            size = ''
            sku = ''
            for index, word in enumerate(text_sep_by_space):
                if index == 0:
                    word = word[3:]
                if word.isdigit():
                    quantity = int(word)
                elif len(word) < 5:
                    size = word
                else:
                    sku = word

                if sku and size and quantity:
                    if (sku, size) in sku_size_quantity_dict:
                        sku_size_quantity_dict[(sku, size)] += quantity
                    else:
                        sku_size_quantity_dict[(sku, size)] = quantity
                    quantity = 0
                    size = ''
                    sku = ''


sku_size_quantity_list = [[i[0], i[1], sku_size_quantity_dict[i]] for i in sku_size_quantity_dict]
data = json.load(open('mapping of skus.json'))

for i in data:
    data[i] = str(data[i])

for i in range(len(sku_size_quantity_list)):
    x = sku_size_quantity_list[i][0]
    if data.get(x):
        sku_size_quantity_list[i][0] = mapping_of_groups[int(data[sku_size_quantity_list[i][0]])]
    else:
        sku_size_quantity_list[i][0] = sku_size_quantity_list[i][0]

sku_size_quantity_list_after_collapse = {}
for i in sku_size_quantity_list:
    set_ = tuple(i[:2])
    if sku_size_quantity_list_after_collapse.get(set_):
        print(sku_size_quantity_list_after_collapse[set_], i)
        sku_size_quantity_list_after_collapse[set_] = sku_size_quantity_list_after_collapse[set_][:2] + [sku_size_quantity_list_after_collapse[set_][2] + i[2]]
    else:
        sku_size_quantity_list_after_collapse[set_] = i

sku_size_quantity_list_after_collapse = sku_size_quantity_list_after_collapse.values()

exporting_dataframe = pd.DataFrame(sku_size_quantity_list_after_collapse)
exporting_dataframe.columns = ['SKU', 'SIZE', 'QUANTITY']
sizes = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL', '4XL']

for col in ['QUANTITY']:
    exporting_dataframe[col] = exporting_dataframe[col].astype(int)

for size in sizes:
    exporting_dataframe = exporting_dataframe._append({'SKU': 'TOTAL', 'SIZE': size, 'QUANTITY': exporting_dataframe[exporting_dataframe['SIZE'] == size]['QUANTITY'].sum()}, ignore_index=True)

exporting_dataframe['SIZE'] = exporting_dataframe['SIZE'].astype('category')
exporting_dataframe['SIZE'] = exporting_dataframe['SIZE'].cat.reorder_categories(new_categories=sizes, ordered=True)

exporting_dataframe = pd.pivot_table(exporting_dataframe, index='SKU', columns='SIZE', values='QUANTITY')
exporting_dataframe = exporting_dataframe.fillna(0)

exporting_dataframe.loc['TOTAL ', :] = exporting_dataframe.loc['TOTAL', :].to_dict()
exporting_dataframe.drop('TOTAL', inplace=True)

exporting_dataframe.to_excel('output.xlsx')
# exporting_dataframe.to_excel('output.xlsx', index=False)