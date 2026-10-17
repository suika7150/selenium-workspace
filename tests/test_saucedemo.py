import os
import time
from selenium import webdriver
# 定位網頁元素工具 By
from selenium.webdriver.common.by import By
# 等待網頁元素工具 WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 讀取 .env 檔工具
from dotenv import load_dotenv

# 讀取 .env 檔案中的環境變數
load_dotenv()

# 讀取環境變數
TARGET_URL = os.getenv("SAUCE_URL")
USERNAME = os.getenv("SAUCE_USERNAME")
PASSWORD = os.getenv("SAUCE_PASSWORD")

# 自動下載 ChromeDriver
driver = webdriver.Chrome()
# Browser Window 最大化
driver.maximize_window()

wait = WebDriverWait(driver, 10)

try:
    # 導向 Sauce Demo
    # 動作停留 3 秒
    driver.get(TARGET_URL)

    # 輸入帳號與密碼，用 ID 定位元素
    print("正在輸入帳號密碼...")
    username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    username_field.send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)

    # 點擊登入按鈕
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_button.click()

    # 登入成功後，抓取畫面上第一個商品的名稱並印出來
    first_item = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".inventory_item_name")))
    print("【成功登入】第一個看到的商品是:", first_item.text)  

    assert first_item.text != "", "錯誤：抓取到的商品名稱為空值！"

    # 檢查有無資料夾並自動建立 images 資料夾
    if not os.path.exists("images"):
        os.makedirs("images")

    # 將截圖存進 images 資料夾中
    driver.save_screenshot("images/screenshot.png")

    # 在當前分頁中打開其他分頁 (新分頁打開 Google)
    driver.execute_script("window.open('https://www.google.com');")

    # driver.window_handles 可以取得 window list，用 index -1 可以取得最後一個
    new_window = driver.window_handles[-1]

    # 切換到新分頁才能操作 
    driver.switch_to.window(new_window)

    # 關閉當前操作的 Window
    driver.close()
    print("操作完成，關閉頁面")

    # 切回 Sauce Demo 分頁
    driver.switch_to.window(driver.window_handles[0])

except Exception as e:
    print(f"測試失敗，原因: {e}")
    # 失敗截圖
    if os.path.exists("images"):
        driver.save_screenshot("images/error.png")
    raise e

finally:
    # 關閉整個 Browser 釋放資源
    print("關閉瀏覽器...")
    driver.quit()
