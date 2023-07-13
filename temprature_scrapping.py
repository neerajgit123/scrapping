from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
today = datetime.now().date()
url = f'https://www.wunderground.com/history/daily/VAPO/date/{today}'
driver.get(url)
time.sleep(4)
html_data = driver.page_source
soup = BeautifulSoup(html_data, "html5lib")

role_attrs = {"role": "rowgroup"}

try:
    table_header = soup.find("thead", attrs=role_attrs)
    table_heading = table_header.find_all("th")

    table_body = soup.find("tbody", attrs=role_attrs)
    table_data = table_body.find_all("td")

    colums = [data.text for data in table_heading]
    rows = []

    for row in range(0, len(table_data), 10):
        row_data = []
        for data in table_data[row : row + 10]:
            row_data.append(data.text)
        rows.append(row_data)

    df = pd.DataFrame(rows, columns=colums)
    df.to_csv(f"{today}_records.csv")
except Exception as e:
    print("No records found")
