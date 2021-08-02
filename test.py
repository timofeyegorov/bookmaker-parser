from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path=r'C:\Users\admin\PycharmProjects\bookmaker-parser\chromedriver.exe')
url = 'https://selenium-python.readthedocs.io/locating-elements.html#locating-by-id'

try:
    driver.get(url=url)
    time.sleep(5)
except Exception as ex:
    print(ex)
finally:
    driver.quit()
