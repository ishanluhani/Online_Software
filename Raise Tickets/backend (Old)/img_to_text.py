import zxingcpp
import requests, json
from PIL import Image
import cv2

data = {}


def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine': 2,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,

                          )
    return r.content.decode()


def calibrate(d):
    global data
    # Use examples
    for s in d:
        lst = d[s]['paths']
        data2 = ['Not Found', 'Not Found', 'Not Found'] # suborder, awb, packet id
        data_path = {'video': [lst[-1]], 'packet id': '', 'product img': [], 'waybill': []}
        if len(lst) > 1:
            for i in lst[:-1]:
                img = cv2.imread(i)
                results = zxingcpp.read_barcodes(img)
                for result in results:
                    result = result.text
                    # print(result)
                    if '_' in result:
                        data2[0] = result
                        data_path['waybill'].append(i)
                    elif result.isdigit() or result.endswith('FPL'):
                        data2[1] = result
                        data_path['waybill'].append(i)
                    else:
                        data2[2] = result
                        data_path['packet id'] = [i]
                x = Image.open(i)
                x.save('D:/ONLINE software/big project/Returns/' + i.split("/")[-1])
                test_file = ocr_space_file(filename='D:/ONLINE software/big project/Returns/' + i.split("/")[-1], api_key='K85194065988957')
                test_file = json.JSONDecoder().decode(test_file)
                # print(test_file['ParsedResults'][0]['TextOverlay']['Lines'])
                if test_file.get('ParsedResults'):
                    for a in test_file['ParsedResults'][0]['TextOverlay']['Lines']:
                        a = a['LineText'].split()
                        for j in a:
                            if 12 <= len(j) and j[:12].isdigit() and not j[12:].isdigit() and data2[0] == 'Not Found':
                                print('Suborder:', j[:12])
                                data2[0] = j[:12]
                                data_path['waybill'].append(i)
                            elif 'COID:' in j:
                                print('shadowfax Suborder:', j[5:])
                                data2[0] = j[5:]
                                data_path['waybill'].append(i)
                                # data_path[0] = i
                            j = j.split('-')[-1]
                            if (10 == len(j) and j.isdigit()) or (12 < len(j) and j.isdigit()) and \
                                    data2[1] == 'Not Found' or j.endswith('FPL'): # for Ecom express, for Xpress bees and Delhivery and Shadowfax
                                print('Awb:', j)
                                data_path['waybill'].append(i)
                                data2[1] = j
                else:
                    data_path['product img'].append(i)
        data_path['waybill'] = list(set(data_path['waybill']))
        data[s] = [data2, data_path]

#
# calibrate({'Group 1': {'paths': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715519.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715529.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715539.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715550.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/VID_20230721_144742 - Copy - Copy.mp4']}})
# print(data)
# for i in data:
#     i = data[i][1]
#     for x in i:
#         print(x, '------->>', i[x])