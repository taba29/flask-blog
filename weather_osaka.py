from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# --- セットアップ ---
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# --- AMeDAS（気温・湿度）取得 ---
url_amedas = "https://www.jma.go.jp/jp/amedas_h/today-62078.html"
driver.get(url_amedas)
time.sleep(3)  # JavaScript読み込み待機
soup = BeautifulSoup(driver.page_source, 'html.parser')

table = soup.find("table", class_="amedas-table")
if table:
    row = table.select("tr")[1]
    cols = row.find_all("td")
    temperature = cols[0].text.strip()
    humidity = cols[3].text.strip()
else:
    temperature = "取得失敗"
    humidity = "取得失敗"
    print("AMeDASのデータテーブルが見つかりませんでした。")

# --- 天気取得 ---
url_weather = "https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=270000"
driver.get(url_weather)

try:
    # 天気情報が読み込まれるまで待機
    wait = WebDriverWait(driver, 10)
    icon = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "forecast-icon")))
    weather = icon.get_attribute("alt")
except Exception as e:
    weather = "取得失敗"
    print("天気の取得でエラー：", e)

driver.quit()

# --- 結果表示 ---
print(f"大阪の現在の気温：{temperature} ℃")
print(f"大阪の現在の湿度：{humidity} ％")
print(f"大阪の現在の天気：{weather}")
