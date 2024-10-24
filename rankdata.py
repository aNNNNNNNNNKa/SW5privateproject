from idlelib.iomenu import encoding
from turtledemo.penrose import start

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

file_path = 'C:/Users/kiusw/Desktop/zap/Rank.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

ids = data['id'].tolist()

start_id = int(input("시작 id 입력 : "))

if start_id in ids:
    start_index = ids.index(start_id)
else:
    print("ERROR")
    exit()

driver_path = 'C:/Users/kiusw/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

try:
    for game_id in ids[start_index:]:
        url = f"https://boardgamegeek.com/boardgame/{game_id}"
        driver.get(url)
        print("URL : {url}")
        time.sleep(3)
finally:
    driver.quit()
