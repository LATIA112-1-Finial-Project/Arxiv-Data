import csv
from lib2to3.pgen2.driver import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 等待元素可見
def wait_until(self, css_selector, timeout=10):
        """Wait for and return the element(s) selected by css_selector."""
        wait = WebDriverWait(self, timeout=timeout)
        is_visible = EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        return wait.until(is_visible)
driver = webdriver.Chrome()

# 定義要爬取的網址列表
urls = ["https://arxiv.org/archive/math", "https://arxiv.org/archive/cs"]

# 指定 CSV 文件的路徑
file_path = r'C:\Users\user\Desktop\for github\Arxiv-Data\Bo\arxiv_reports.csv'

# 開啟 CSV 文件，指定列名稱
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Year', 'Article', 'Cross-lists', 'Total']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 寫入列名稱
    writer.writeheader()

    for url in urls:
        # 打開目標網站
        driver.get(url)

        # 找到包含年份的元素
        year_elements = driver.find_elements(By.CSS_SELECTOR, '.is-size-7.has-text-weight-bold')

        article_elements = driver.find_elements(By.CSS_SELECTOR, 'b')
        cross_lists_elements = driver.find_elements(By.CSS_SELECTOR, 'i')

        # 提取並寫入CSV文件
        for year_element, article_element, cross_lists_element in zip(year_elements, article_elements, cross_lists_elements):
            year_text = year_element.text.strip()
            article_text = article_element.text.strip()
            cross_lists_text = cross_lists_element.text.strip()

            # 計算總數
            total_text = str(int(article_text) + int(cross_lists_text))

            writer.writerow({'Year': year_text, 'Article': article_text, 'Cross-lists': cross_lists_text, 'Total': total_text})

# 關閉瀏覽器視窗
driver.quit()