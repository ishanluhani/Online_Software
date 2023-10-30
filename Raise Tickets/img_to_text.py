import zxingcpp
import requests, json
from PIL import Image
import cv2
import video_compress


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
        print(lst, 'gk')
        try:
            data_path = {'video': [lst[-1]], 'packet id': [], 'product img': [], 'waybill': []}
            if len(lst) > 1:
                print(lst)
                if lst[-2].split('.')[-1] == 'mp4':
                    ind = 2
                else:
                    ind = 1
                for i in lst[:-ind]:
                    y = Image.open(i)
                    y = y.resize((600, 600))
                    y.save(i)
                    img = cv2.imread(i)
                    print(i)
                    results = zxingcpp.read_barcodes(img)
                    has_entered = False
                    for result in results:
                        result = result.text
                        # print(result)
                        if '_' in result:
                            data2[0] = result
                            data_path['waybill'].append(i)
                            has_entered = True
                        elif result.isdigit() or result.endswith('FPL'):
                            data2[1] = result
                            data_path['waybill'].append(i)
                            has_entered = True
                        else:
                            data2[2] = result
                            data_path['packet id'] = [i]
                            has_entered = True
                    x = Image.open(i)
                    x.save('D:/ONLINE Data/Online Software/Raise Tickets/Returns/' + i.split("/")[-1])
                    test_file = ocr_space_file(filename='D:/ONLINE Data/Online Software/Raise Tickets/Returns/' + i.split("/")[-1], api_key='K85194065988957')
                    test_file = json.JSONDecoder().decode(test_file)
                    print(test_file)
                    # print(test_file['ParsedResults'][0]['TextOverlay']['Lines'])
                    if test_file['ParsedResults'][0]['TextOverlay']['Lines']:
                        for a in test_file['ParsedResults'][0]['TextOverlay']['Lines']:
                            a = a['LineText'].split()
                            for j in a:
                                print(len(j) > 12, j[:12].isdigit(), j[13:].isdigit(), data2[0] == 'Not Found', j)
                                if len(j) >= 12 and j[:12].isdigit() and not j[13:].isdigit() and data2[0] == 'Not Found':
                                    print('Suborder:', j[:12])
                                    data2[0] = j[:12]
                                    data_path['waybill'].append(i)
                                    has_entered = True
                                elif 'COID:' in j:
                                    print('shadowfax Suborder:', j[5:])
                                    data2[0] = j[5:]
                                    data_path['waybill'].append(i)
                                    has_entered = True
                                    # data_path[0] = i
                                if not j[0].isdigit() and j[-1].isdigit():
                                    data_path['packet id'] = [i]
                                    has_entered = True
                                j = j.split('-')[-1]
                                if (10 == len(j) and j.isdigit()) or (12 < len(j) and j.isdigit()) and \
                                        data2[1] == 'Not Found' or j.endswith('FPL'): # for Ecom express, for Xpress bees and Delhivery and Shadowfax
                                    print('Awb:', j)
                                    data_path['waybill'].append(i)
                                    data2[1] = j
                                    has_entered = True
                    if not has_entered:
                        data_path['product img'].append(i)
            data_path['waybill'] = list(set(data_path['waybill']))
            data[s] = [data2, data_path]
        except Exception as e:
            print(e, 'errorrrr')

#
# calibrate({'Group 1': {'paths': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715519.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715529.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715539.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715550.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/VID_20230721_144742 - Copy - Copy.mp4']}})
# print(data)
# for i in data:
#     i = data[i][1]
#     for x in i:
#         print(x, '------->>', i[x])