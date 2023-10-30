import pandas as pd


def choose(parameters, data):
    # for i in parameters:
    #     if i != 'link' and i != 'name' and i != 'description':
    #         data[i] = data[i][:int(parameters[i])]
    return data


table = pd.read_csv('D:/ONLINE Data/Online Software/Raise Tickets/tickets.csv')
tickets = table.iloc[:, 0].to_list()


def run(chosen, data):
    return choose(table[table['name'] == chosen], data), table[table['name'] == chosen][['description', 'link']]


if __name__ == '__main__':
    print(([['856647961520', '14907906162643', 'DLVPCE167893346'], {'video': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/VID_20230721_144742 - Copy.mp4'], 'packet id': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715550.jpg'], 'product img': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715519.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715529.jpg'], 'waybill': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715539.jpg']}]))