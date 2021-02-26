
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.proxy import Proxy
from selenium.common.exceptions import TimeoutException
from time import sleep
import logging
import xlsxwriter 


# https://www.eventseye.com/

readed = []  # readed user-agent bilgisi tutucak

logging.basicConfig(filename='AppLog.log', level=logging.WARNING)
logging.getLogger()


def exceptLog(msg):
    try:
        logging.exception(msg)
        return True
    except Exception as e:
        logging.exception(e)
    return False


def userAgentRead():
    try:
        with open("user-agent.txt", "r", encoding="utf-8") as file:
            reads = file.readlines()
            for read in reads:
                readed.append(read.strip())
            return True
    except Exception as e:
        exceptLog(e)
    return False

# User-Agent Dosyamı okuyorum


def getUserAgent():
    if len(readed) > 1:
        userAgent = readed[0]
        readed.remove(userAgent)
    else:
        userAgentRead()
        userAgent = readed[0]
        readed.remove(userAgent)
    return userAgent

# selenium modülümün hangi bilgiler ile websiteyi ziyaret ediceğini giriyorum.


def getProfile():
    if not len(readed) > 0:
        userAgentRead()
    useragent = getUserAgent()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", useragent)    
    profile.update_preferences()
    return profile

def main():
    firefoxProfile = getProfile()
    browser = webdriver.Firefox(firefox_profile=firefoxProfile)
    sleep(2)
    browser.get("https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Germany")
    # browserın tam açılmasını bekliyorum
    # website yüklendikten belirli bir süre sonra işlem yapmamı imkan sağlar.
    print("5 saniye bekleyiniz")
    sleep(2)
    wait = WebDriverWait(browser, 5)
    #document.querySelectorAll("body table ul>li>a")[111].textContent = "Bad Frankenhausen/Kyffhäuser"
    # Bazı verilerin içinde / karakterinden sonrasını yok etmen gerek
    try:
        datas = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body table ul>li>a")))
        orjinalDatas = []
        for data in datas:
            print(data.text)
            orjinalDatas.append(data.text)
            if data.text == "Zwönitz":
                break
        print(orjinalDatas)
        with open("GermanyTown.txt","w",encoding="utf8") as file:
            for data in orjinalDatas:
                file.writelines(data + "\n")

    except Exception as e:
        print(e)
    finally:
        input("BROWSER KAPANICAK:")
        browser.close()

if __name__ == "__main__":
    main()