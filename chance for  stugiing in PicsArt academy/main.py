""" DocString """
import time
from MyOwnDB import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

url = 'https://www.coinbase.com/ru/price'
options = webdriver.ChromeOptions()
# options.set_headless(True)
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
coinbaseRates = MyOwnDB("./coinbase.db")
different = MyOwnDB("./different.db")
attached = []
time.sleep(5)
while True:
    for i in range(1, 30):
        time.sleep(5)
        crypto = driver.find_element_by_xpath("/html/body/div[1]/div/div/main/div[1]/table/tbody/tr[%s]" % i).text
        crypto = crypto.replace('\uea3f', "").split('\n')
        if crypto[0] == '':
            crypto = crypto[1:]
        # attached.append(crypto.replace('\uea3f', "").split('\n'))
        attached.append(crypto)
        # get new price by parsing
        new_price = str(attached[i - 1][2][:-7]).replace(' ', '')
        # check databases has all values crypto after parsing and pass changes to other database
        if len(coinbaseRates.allItems()) >= 15 and new_price != '':
            # get old price from database and cast to float
            old_price = coinbaseRates.get(attached[i - 1][0])
            old_price = str(old_price).replace(' ', '')
            print(new_price, "||", old_price)
            difference = float(new_price) - float(old_price)
            different.changeValue(str(attached[i - 1][0]), difference)
            coinbaseRates.changeValue(str(attached[i - 1][0]), new_price)  # attached[i - 1][2][:-7])
        else:
            coinbaseRates.changeValue(str(attached[i - 1][0]), 0)  # attached[i - 1][2][:-7])
        coinbaseRates.dumpDB()
        different.dumpDB()
    try:
        coinbaseRates.update_excel("CoinBase")
        different.update_excel("different")
    except:
        coinbaseRates.to_excel('CoinBase')
        different.to_excel('different')
    print(attached)
    attached = []
    time.sleep(15)
    driver.refresh()
