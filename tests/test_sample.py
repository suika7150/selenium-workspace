import time
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config


@allure.epic("UI 自動化測試")
@allure.feature("瀏覽器基本導航操作")
def test_browser_navigation():
    """測試瀏覽器基本導航（前進、後退、分頁切換與截圖）"""
    # 自動下載 ChromeDriver
    driver = webdriver.Chrome()

    # Browser Window 最大化
    driver.maximize_window()

    try:
        with allure.step("導向 Google 頁面"):
            driver.get("https://google.com")
            time.sleep(3)

        with allure.step("導向 YouTube 頁面"):
            driver.get("https://youtube.com")
            time.sleep(3)

        with allure.step("頁面後退回 Google"):
            driver.back()
            time.sleep(3)

        with allure.step("頁面前進回 YouTube"):
            driver.forward()
            time.sleep(3)

        with allure.step("開啟新分頁並切換"):
            driver.execute_script("window.open('https://www.google.com');")
            time.sleep(3)
            new_window = driver.window_handles[-1]
            driver.switch_to.window(new_window)

        with allure.step("儲存截圖至 images 目錄"):
            Config.IMAGE_DIR.mkdir(parents=True, exist_ok=True)
            driver.save_screenshot(str(Config.IMAGE_DIR / "sample_screenshot.png"))

        with allure.step("關閉新分頁"):
            driver.close()
            print("操作完成，關閉頁面")
            time.sleep(3)

    finally:
        # 關閉整個 Browser 釋放資源
        driver.quit()
