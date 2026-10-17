import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

# 自動下載 ChromeDriver
driver = webdriver.Chrome()

# Browser Window 最大化
driver.maximize_window()

try:
    # 導向 https://www.google.com
    # 動作停留 3 秒
    driver.get("https://google.com")
    time.sleep(3)

    # 導向 https://youtube.com
    driver.get("https://youtube.com")
    time.sleep(3)

    # 頁面後退，https://www.google.com
    driver.back()
    time.sleep(3)

    # 頁面前進，https://youtube.com
    driver.forward()
    time.sleep(3)

    # 在當前分頁中打開其他分頁 (新分頁打開 Google)
    driver.execute_script("window.open('https://www.google.com');")
    time.sleep(3)

    # driver.window_handles 可以取得 window list，用 index -1 可以取得最後一個
    new_window = driver.window_handles[-1]

    # 切換到最新的 Window 才能操作
    driver.switch_to.window(new_window)

    # 檢查有無資料夾並自動建立 images 資料夾
    Config.IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # 將截圖存進 images 資料夾中
    driver.save_screenshot(str(Config.IMAGE_DIR / "sample_screenshot.png"))

    # 關閉當前操作的 Window
    driver.close()
    print("操作完成，關閉頁面")
    time.sleep(3)
finally:
    # 關閉整個 Browser
    driver.quit()