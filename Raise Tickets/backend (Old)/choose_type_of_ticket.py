import pandas


def choose(parameters, data):
    for i in parameters:
        if i != 'link' and i != 'name' and i != 'description':
            data[i] = data[i][:int(parameters[i])]


def run(data):
    table = pandas.read_excel('D:/ONLINE software/big project/tickets.xlsx')

    num = int(input('Enter number: '))-1
    ans = table.iloc[num].to_dict()

    choose(ans, data[1])
    description = ans['description']
    description = description.replace('SUB', data[0][0])
    description = description.replace('AWBNO', data[0][1])
    description = description.replace('PACKET', data[0][2])
    data.append(description)
    return data


if __name__ == '__main__':
    print(run([['856647961520', '14907906162643', 'DLVPCE167893346'], {'video': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/VID_20230721_144742 - Copy.mp4'], 'packet id': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715550.jpg'], 'product img': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715519.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715529.jpg'], 'waybill': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715539.jpg']}]))