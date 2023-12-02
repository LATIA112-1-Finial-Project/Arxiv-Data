#!/usr/bin/env python
# coding: utf-8

# In[24]:


import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
import os

def wait_for_element_visibility(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def get_categorys_and_links(driver, field):
    categorys = []
    category_links = []

    h2_element = wait_for_element(driver, (By.XPATH, f'//h2[text()="{field}"]'))
    ul_elements = h2_element.find_elements(By.XPATH, "./following-sibling::ul")
    li_elements = ul_elements[0].find_elements(By.TAG_NAME, "li")

    for li_element in li_elements:
        category_element = li_element.find_element(By.TAG_NAME, "a")
        categorys.append(category_element.text)
        category_links.append(category_element.get_attribute("href"))

    return categorys, category_links

def get_years_and_links(driver):
    years = []
    year_links = []

    year_list_element = wait_for_element(
        driver, (By.XPATH, '//li[contains(text(), "Article statistics by year:")]')
    )

    year_link_elements = year_list_element.find_elements(By.TAG_NAME, "a")

    for year_element in year_link_elements:
        year_link = str(year_element.get_attribute("href"))
        year_link = os.path.dirname(year_link) + "/" + year_element.text[-2:]

        years.append(year_element.text)
        year_links.append(year_link)

    return years, year_links

def get_articles_and_cross_lists(driver):
    totals_element = wait_for_element(
        driver, (By.XPATH, '//p[contains(text(), "totals:")]')
    )

    totals_text = totals_element.text

    articles_match = re.search(r"(\d+) articles", totals_text)
    cross_lists_match = re.search(r"(\d+) cross-lists", totals_text)

    articles_count = int(articles_match.group(1)) if articles_match else 0
    cross_lists_count = int(cross_lists_match.group(1)) if cross_lists_match else 0

    return articles_count, cross_lists_count

def crawl_category_data(url, field, chrome_options, final_table_writer):
    # 初始化檔案名稱
    file_name = f"{field}_data.csv"

    # 設定等待時間
    wait_time = 5

    # 初始化 WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)  # 開啟網頁

    # 獲取子領域的名稱和相應的超連結
    categorys, category_links = get_categorys_and_links(driver, field)

    for category, category_link in zip(categorys, category_links):
        print(f"Crawling Category {category}...")

        # 訪問子領域的超連結
        driver.get(category_link)
        wait_for_element_visibility(driver, (By.ID, "content"), timeout=20)

        # 獲取所有年份和相應的超連結
        years, year_links = get_years_and_links(driver)
        with open(file_name, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Year", "Articles", "Cross-lists", "Total"])

            for year, year_link in zip(years, year_links):
                # 依序爬取每個年份
                driver.get(year_link)
                wait_for_element_visibility(driver, (By.ID, "content"), timeout=20)

                # 獲取文章和交叉列表的數量，並計算總數
                articles, cross_lists = get_articles_and_cross_lists(driver)
                total = articles + cross_lists

                # 寫入 csv 檔案
                csv_writer.writerow([year, articles, cross_lists, total])

                # Update the final table
                final_table_writer.writerow([field, year, articles, cross_lists, total])

        print(f"Succeed! {file_name} has been created.\n")

    # 關閉 WebDriver
    driver.quit()

if __name__ == "__main__":
    url = "https://arxiv.org/"
    fields = ["Physics","Economics", "Electrical Engineering and Systems Science", "Statistics", "Quantitative Finance", "Quantitative Biology"]

    # 設定 WebDriver，使用 Chrome 瀏覽器在背景執行
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 不開啟實體瀏覽器

    # 初始化 final table 的 CSV 寫入器
    with open("final_data.csv", "w", newline="") as final_csvfile:
        final_table_writer = csv.writer(final_csvfile)
        final_table_writer.writerow(["Field", "Year", "Articles", "Cross-lists", "Total"])

        for field in fields:
            crawl_category_data(url, field, chrome_options, final_table_writer)
            # 在每個 FIELD 之間增加等待時間（10秒）
            time.sleep(10)
