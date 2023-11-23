from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import (
    expected_conditions as EC,
)
import re
import os
import csv


def wait_for_element(driver, locator, timeout=7):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


def wait_for_elements(driver, locator, timeout=7):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located(locator)
    )


def get_categorys_and_links(driver, field):
    categorys = []
    category_links = []

    h2_elements = wait_for_element(driver, (By.XPATH, f'//h2[text()="{field}"]'))
    ul_elements = h2_elements.find_elements(By.XPATH, "./following-sibling::ul")
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

    # 使用正則表達式來匹配數字
    articles_match = re.search(r"(\d+) articles", totals_text)
    cross_lists_match = re.search(r"(\d+) cross-lists", totals_text)

    # 取出匹配到的數字部分，若無匹配則返回 None
    articles_count = int(articles_match.group(1)) if articles_match else 0
    cross_lists_count = int(cross_lists_match.group(1)) if cross_lists_match else 0

    return articles_count, cross_lists_count


if __name__ == "__main__":
    # Variables
    url = "https://arxiv.org/"
    field = "Mathematics"

    # Set up driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    categorys, category_links = get_categorys_and_links(driver, field)

    for category, category_link in zip(categorys, category_links):
        print(f"Crawling Category {category}...")

        file_name = field + "_" + category.replace(" ", "_").replace("-", "_") + ".csv"
        file_name = re.sub(r"_+", "_", file_name)

        driver.get(category_link)
        wait_for_element(driver, (By.ID, "content"))

        years, year_links = get_years_and_links(driver)
        with open(file_name, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Year", "Articles", "Cross-lists", "Total"])

            for year, year_link in zip(years, year_links):
                driver.get(year_link)
                wait_for_element(driver, (By.ID, "content"))

                articles, cross_lists = get_articles_and_cross_lists(driver)
                total = articles + cross_lists

                csv_writer.writerow([year, articles, cross_lists, total])

        print(f"Succeed! {file_name} has been created.\n")

    driver.quit()
