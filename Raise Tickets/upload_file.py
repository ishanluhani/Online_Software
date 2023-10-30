from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def run_file(data, description='', link=''):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)

    driver.get(link)
    sleep(10)
    # driver.get('https://youtube.com')
    try:
        email = driver.find_element_by_id('mui-1')
        email.send_keys('neetuluhani@gmail.com')
        password = driver.find_element_by_id('mui-2')
        password.send_keys('1@Kajukishmish')
        driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/form/button[2]').send_keys("\n")
    except:
        pass

    try:

        data_grouper = data[1]
        real_data = data[0]

        description = description.replace('AWBNO', real_data[1])

        sleep(5)

        driver.get('https://supplier.meesho.com/panel/v3/new/payouts/cicpk/support/1/1/create')
        sleep(5)
        driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[2]/div/input').send_keys(real_data[0])
        driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[4]/div/input').send_keys(real_data[2])
        driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[15]/div/textarea[1]').send_keys(description)

        packet_id = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[7]/div/label/input[@type='file']")
        for i in data_grouper['packet id']:
            packet_id.send_keys(i)
            sleep(2)
        product_upload = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[9]/div/label/input[@type='file']")
        for i in data_grouper['product img']:
            product_upload.send_keys(i)
            sleep(2)
        waybill_upload = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[11]/div/label/input[@type='file']")
        for i in data_grouper['waybill']:
            waybill_upload.send_keys(i)
            sleep(2)
        video_upload = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[13]/div/label/input[@type='file']")
        for i in data_grouper['video']:
            video_upload.send_keys(i)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run_file({'Group 1': [['856647961520', '14907906162643', 'DLVPCE167893346'], {'video': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/VID_20230721_144742 - Copy.mp4'], 'packet id': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715550.jpg'], 'product img': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715519.jpg', '//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715529.jpg'], 'waybill': ['//RASPBERRYPI/128gbSSD/returns ex/Group 1/1689935715539.jpg']}]})
