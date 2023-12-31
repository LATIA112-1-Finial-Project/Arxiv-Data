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


def wait_for_element(driver, locator, timeout=5):
    """
    等待元素出現，直到超時或元素可見。

    Args:
        driver: WebDriver 實例
        locator: 元素定位器，例如 (By.ID, "element_id")
        timeout: 等待的最大秒數

    Returns:
        WebElement: 返回找到的元素
    """
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


def wait_for_elements(driver, locator, timeout=5):
    """
    等待所有元素出現，直到超時或元素可見。

    Args: 同 wait_for_element

    Returns: 同 wait_for_element
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located(locator)
    )


def get_categorys_and_links(driver, field):
    """
    獲取子領域的名稱和相應的超連結。

    Args:
        driver: WebDriver 實例
        field: 要爬取的領域

    Returns:
        tuple: 包含分類列表和鏈接列表的元組
    """
    categorys = []
    category_links = []

    # 找到領域名稱對應的 h2 元素
    h2_element = wait_for_element(driver, (By.XPATH, f'//h2[text()="{field}"]'))

    # 找到 h2 元素的下一個 ul 元素，再找到 ul 元素下的所有 li 元素
    ul_elements = h2_element.find_elements(By.XPATH, "./following-sibling::ul")
    li_elements = ul_elements[0].find_elements(By.TAG_NAME, "li")

    for li_element in li_elements:
        # 找到 li 元素下的 a 元素，並取出文字和超連結
        category_element = li_element.find_element(By.TAG_NAME, "a")

        categorys.append(category_element.text)
        category_links.append(category_element.get_attribute("href"))

    return categorys, category_links


def get_years_and_links(driver):
    """
    獲取所有年份和相應的超連結。

    Args:
        driver: WebDriver 實例

    Returns:
        tuple: 包含年份列表和鏈接列表的元組
    """
    years = []
    year_links = []

    # 找到包含年份列表的 ul 元素
    year_list_element = wait_for_element(
        driver, (By.XPATH, '//li[contains(text(), "Article statistics by year:")]')
    )

    # 找到 ul 元素下的所有 a 元素
    year_link_elements = year_list_element.find_elements(By.TAG_NAME, "a")

    for year_element in year_link_elements:
        # 取出 a 元素中的年分與超連結，並修正超連結
        year_link = str(year_element.get_attribute("href"))
        year_link = os.path.dirname(year_link) + "/" + year_element.text[-2:]

        years.append(year_element.text)
        year_links.append(year_link)

    return years, year_links


def get_articles_and_cross_lists(driver):
    """
    獲取文章和交叉列表的數量。

    Args:
        driver: WebDriver 實例

    Returns:
        tuple: 包含文章和交叉列表數量的元組
    """

    # 找到包含文章和交叉列表數量的 p 元素
    totals_element = wait_for_element(
        driver, (By.XPATH, '//p[contains(text(), "totals:")]')
    )

    totals_text = totals_element.text

    # 使用正則表達式匹配文章和交叉列表數量
    articles_match = re.search(r"(\d+) articles", totals_text)
    cross_lists_match = re.search(r"(\d+) cross-lists", totals_text)

    # 取出匹配到的數字部分，若無匹配則返回 0
    articles_count = int(articles_match.group(1)) if articles_match else 0
    cross_lists_count = int(cross_lists_match.group(1)) if cross_lists_match else 0

    return articles_count, cross_lists_count


if __name__ == "__main__":
    # 要爬取的網址和領域名稱
    url = "https://arxiv.org/archive/cs"
    field = "Computing Research Repository"

    # 設定 WebDriver，使用Chrome瀏覽器在背景執行
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 不開啟實體瀏覽器
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)  # 開啟網頁

    # 使用 get_years_and_links 獲取所有年份和相應的超連結
    years, year_links = get_years_and_links(driver)

    # 建立 CSV 檔案
    file_name = "outputs/Computer_Science_Computing_Research_Repository.csv"

    with open(file_name, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Year", "Articles", "Cross-lists", "Total"])

        for year, year_link in zip(years, year_links):
            driver.get(year_link)
            wait_for_element(driver, (By.ID, "content"))

            # 獲取文章和交叉列表的數量, 並計算總數
            articles, cross_lists = get_articles_and_cross_lists(driver)
            total = articles + cross_lists

            # 寫入 csv 檔案
            csv_writer.writerow([year, articles, cross_lists, total])

    print(f"Succeed! {file_name} has been created.\n")

    driver.quit()  # 關閉瀏覽器
