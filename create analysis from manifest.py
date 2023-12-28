from PyPDF2 import PdfReader
from tkinter.filedialog import askdirectory
import pandas as pd
import os


# Defining variable that will be used Later on
sku_size_quantity_dict = {}
colors = ['Multicolor', 'Teal', 'Grey', 'Navy', 'Blue', 'White', 'Beige', 'Maroon', 'Orange', 'Brown', 'Black', 'Yellow', 'Red', 'Pink', 'NA', 'Green', 'OVERSIZE']
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
exporting_dataframe = pd.DataFrame(sku_size_quantity_list)
exporting_dataframe.columns = ['SKU', 'SIZE', 'QUANTITY']
sizes = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL', '4XL']

for col in ['QUANTITY']:
    exporting_dataframe[col] = exporting_dataframe[col].astype(int)

for size in sizes:
    exporting_dataframe = exporting_dataframe._append({'SKU': 'TOTAL', 'SIZE': size, 'QUANTITY': exporting_dataframe[exporting_dataframe['SIZE'] == size]['QUANTITY'].sum()}, ignore_index=True)

exporting_dataframe['SIZE'] = exporting_dataframe['SIZE'].astype('category')
exporting_dataframe['SIZE'] = exporting_dataframe['SIZE'].cat.reorder_categories(new_categories=sizes,
                                                                                                ordered=True)

exporting_dataframe = pd.pivot_table(exporting_dataframe, index='SKU', columns='SIZE', values='QUANTITY')
exporting_dataframe = exporting_dataframe.fillna(0)

exporting_dataframe.loc['TOTAL ', :] = exporting_dataframe.loc['TOTAL', :].to_dict()
exporting_dataframe.drop('TOTAL', inplace=True)

print(exporting_dataframe)
exporting_dataframe.to_excel('output.xlsx')
# exporting_dataframe.to_excel('output.xlsx', index=False)