from selenium import webdriver
# 定位網頁元素工具 By
from selenium.webdriver.common.by import By
# 等待網頁元素工具 WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
import allure


@allure.epic("UI 自動化測試")
@allure.feature("Sauce Demo 登入與商品操作")
def test_sauce_demo_login():
    """測試 Sauce Demo 登入流程、抓取首個商品並保存截圖"""
    # 自動下載 ChromeDriver
    driver = webdriver.Chrome()
    # Browser Window 最大化
    driver.maximize_window()

    # 調用 Config 設定秒數
    wait = WebDriverWait(driver, Config.TIMEOUT)

    try:
        with allure.step("導向 Sauce Demo 網站"):
            driver.get(Config.TARGET_URL)

        with allure.step("輸入使用者名稱與密碼"):
            print("正在輸入帳號密碼...")
            username_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
            username_field.send_keys(Config.USERNAME)
            driver.find_element(By.ID, "password").send_keys(Config.PASSWORD)

        with allure.step("點擊登入按鈕"):
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
            login_button.click()

        with allure.step("驗證首個商品名稱並確認非空值"):
            first_item = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".inventory_item_name")))
            print("【成功登入】第一個看到的商品是:", first_item.text)
            assert first_item.text != "", "錯誤：抓取到的商品名稱為空值"

        with allure.step("儲存成功截圖"):
            Config.IMAGE_DIR.mkdir(parents=True, exist_ok=True)
            driver.save_screenshot(str(Config.IMAGE_DIR / "screenshot.png"))

        with allure.step("開啟新分頁瀏覽 Google 並關閉"):
            driver.execute_script("window.open('https://www.google.com');")
            new_window = driver.window_handles[-1]
            driver.switch_to.window(new_window)
            driver.close()
            print("操作完成，關閉頁面")
            driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"測試失敗，原因: {e}")
        # 失敗截圖
        Config.IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(Config.IMAGE_DIR / "error.png"))
        raise e

    finally:
        # 關閉整個 Browser 釋放資源
        print("關閉瀏覽器...")
        driver.quit()
