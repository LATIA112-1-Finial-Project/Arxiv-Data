import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

def scrape_arxiv_with_selenium(category, year):
    # Create Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1200x600')

    # Specify the path to your ChromeDriver executable
    driver_path = "C:/path/to/chromedriver.exe"
    options.add_argument(f"executable_path={driver_path}")

    # Use a different name for the WebDriver instance to avoid conflict
    wd = webdriver.Chrome(options=options)

    # Visit the arXiv webpage
    base_url = f"https://arxiv.org/list/{category}/{year}"
    wd.get(base_url)

    try:
        table = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-table'))
        )
    except Exception as e:
        print("Error waiting for the table element:", e)
        wd.quit()
        return

    time.sleep(5)

    rows = table.find_elements(By.TAG_NAME, 'tr')[1:]

    data = []
    headers = ['Title', 'Authors', 'Link']

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        title = columns[0].text
        authors = columns[1].text
        link = columns[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
        data.append([title, authors, link])

    # Close the WebDriver
    wd.quit()

    # Save as a CSV file
    df = pd.DataFrame(data, columns=headers)
    file_path = os.path.join(os.path.expanduser('~'), 'Desktop', f"{category}_{year}_arxiv.csv")
    df.to_csv(file_path, index=False)
    print(f"{category}_{year}_arxiv.csv has been saved to {file_path}.")

if __name__ == "__main__":
    categories = ['math', 'cs']
    years = ['21', '20']

    for category in categories:
        for year in years:
            scrape_arxiv_with_selenium(category, year)