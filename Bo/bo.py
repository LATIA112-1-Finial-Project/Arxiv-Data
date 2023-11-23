import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# 設定瀏覽器
driver = webdriver.Chrome()

# 定義要爬取的網址列表
urls = ["https://arxiv.org/archive/math", "https://arxiv.org/archive/cs"]

# 開啟CSV文件，指定列名稱
with open('arxiv_reports.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['網址', '年份', '報告數']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 寫入列名稱
    writer.writeheader()

    for url in urls:
        # 打開目標網站
        driver.get(url)

        # 找到包含年份和報告數的元素
        year_elements = driver.find_elements(By.CSS_SELECTOR, '.is-size-7.has-text-weight-bold')
        report_elements = driver.find_elements(By.CSS_SELECTOR, '.is-size-7.has-text-weight-light')

        # 提取並寫入CSV文件
        for year, reports in zip(year_elements, report_elements):
            year_text = year.text.strip()
            reports_text = reports.text.strip()
            writer.writerow({'網址': url, '年份': year_text, '報告數': reports_text})

# 關閉瀏覽器視窗
driver.quit()