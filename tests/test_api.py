import pytest
import requests
import allure

# 定義測試目標伺服器網址
BASE_URL = "https://jsonplaceholder.typicode.com"

# Fixture 前置與後置處理
@pytest.fixture(scope="module")
def api_session():
    """
    【什麼是 Fixture？】
    Fixture 是 pytest 用來準備測試環境（Setup）與收拾善後（Teardown）的強大機制。
    
    【參數說明】
    - scope="module"：代表整個測試檔案只會建立一次這個 session，
      所有測試案例共用它，直到本檔案全部測試結束才關閉，能大幅提升執行效率。
    
    【為什麼用 requests.Session() 而不是直接 requests.get()？】
    1. 連線池優化 (Connection Pooling)：底層自動複用 TCP 連線，減少每次握手的時間。
    2. 全域設定共享：可以在 session 上統一預設 Headers、Cookies、Auth Token，
       後續發送請求就不需要每次重複傳遞。
    """
    # 前置準備：建立 Session 物件並設定預設的 Header
    session = requests.Session()
    session.headers.update({
        # 告知伺服器發送的資料格式是 JSON (編碼 UTF-8)
        "Content-Type": "application/json; charset=UTF-8",
        # 告知伺服器預期接收的回傳格式也是 JSON
        "Accept": "application/json"
    })

    # 交出控制權 (yield)：把建立好的 session 傳給測試函式使用
    # yield 之前的程式碼，在測試開始前執行
    # yield 之後的程式碼，在測試結束後執行
    yield session

    # 後置清理：測試執行結束後，關閉連線釋放系統資源
    session.close()

# - Epic:最高層級分類 (如：API 練習專案、UI 測試專案)
# - Feature:中層功能模組 (如：JSONPlaceholder API、購物車功能)
# - Story:最細項的測試情境，會直接顯示在報告中的側邊欄
@allure.epic("API 練習專案")
@allure.feature("JSONPlaceholder API 測試")
class TestJsonPlaceholderAPI:

    # GET 取得列表
    @allure.story("GET 請求 - 查詢列表 (GET /posts)")
    def test_get_all_posts(self, api_session):
        """
        【測試目的】驗證能否正常取得整批文章清單。
        """
        # with allure.step() 可以把測試拆解成清楚的步驟，顯示在 Allure 報告中
        with allure.step("步驟 1：發送 GET 請求取得所有文章"):
            # timeout=10 避免伺服器無回應時，測試程式永遠卡死
            response = api_session.get(f"{BASE_URL}/posts", timeout=10)

        with allure.step("步驟 2：驗證 HTTP 狀態碼與標頭 (Header)"):
        
            # 逗號後面為自訂失敗提示訊息
            assert response.status_code == 200, f"預期狀態碼 200，但收到 {response.status_code}"
            # headers 資訊
            content_type = response.headers.get("Content-Type", "")
            assert "application/json" in content_type, f"預期 Content-Type 為 JSON，實際收到: {content_type}"

        with allure.step("步驟 3：驗證回傳的資料結構與筆數"):
           
            data = response.json()
            # isinstance(物件, 型別) 用來檢查資料型別是否正確
            assert isinstance(data, list), "文章列表的回傳根節點型別應為清單 (list)"
            assert len(data) > 0, "文章清單不應為空"
            
            print(f"\n【GET 列表成功】共取得 {len(data)} 筆文章資料，第 1 筆標題：{data[0]['title']}")

    # GET 查詢單一資源
    @allure.story("GET 請求 - 查詢單一資源 (GET /posts/{id})")
    def test_get_single_post(self, api_session):
        """
        【測試目的】驗證帶入特定 ID 能否精準查出對應的單篇文章。
        """
        post_id = 1
        with allure.step(f"步驟 1：發送 GET 請求取得 ID={post_id} 的文章"):
            
            response = api_session.get(f"{BASE_URL}/posts/{post_id}", timeout=10)

        with allure.step("步驟 2：驗證回傳資料正確性"):

            assert response.status_code == 200, "取得單筆資料失敗"
            post = response.json()
            # 驗證 ID 是否正確
            assert post["id"] == post_id, f"文章 ID 應為 {post_id}，但取得 {post['id']}"
            # 驗證必要的 Key 是否存在
            assert "userId" in post, "回傳資料缺少必要欄位 'userId'"
            assert "title" in post, "回傳資料缺少必要欄位 'title'"
            assert "body" in post, "回傳資料缺少必要欄位 'body'"
            # 驗證欄位的資料型態
            assert isinstance(post["title"], str), "title 欄位必須為字串 (str)"
            assert len(post["title"]) > 0, "title 欄位內容不應為空字串"
            
            print(f"\n【GET 單筆成功】ID={post['id']} | 標題: {post['title']}")

    # GET 帶查詢參數
    @allure.story("GET 請求 - 查詢參數篩選 (GET /posts?userId=1)")
    def test_get_posts_with_query_params(self, api_session):
        """
        【測試目的】驗證使用 Query Parameters 篩選特定使用者的文章。
        """
        query_params = {"userId": 1}
        with allure.step(f"步驟 1：帶入查詢參數 {query_params} 發送 GET 請求"):

            response = api_session.get(f"{BASE_URL}/posts", params=query_params, timeout=10)

        with allure.step("步驟 2：驗證篩選結果的精確度"):
            assert response.status_code == 200
            posts = response.json()
            assert isinstance(posts, list)
            assert len(posts) > 0, "篩選結果不應為空"
            
            # 檢查回傳的每一篇文章 userId 都確實是 1
            for item in posts:
                assert item["userId"] == 1, f"資料錯誤：找到不屬於 userId=1 的文章 (收到 userId={item['userId']})"
                
            print(f"\n【GET 篩選成功】userId=1 的文章共有 {len(posts)} 篇，全部資料驗證無誤")

    # 反向測試 / 異常情境
    @allure.story("GET 請求 - 異常情況測試 (404 Not Found)")
    def test_get_post_not_found(self, api_session):
        """
        【測試目的】反向測試：請求不存在的資料，確認後端防呆與錯誤處理正常。
        """
        not_exist_id = 99999
        with allure.step(f"步驟 1：請求不存在的文章 ID={not_exist_id}"):
            response = api_session.get(f"{BASE_URL}/posts/{not_exist_id}", timeout=10)

        with allure.step("步驟 2：驗證回傳 404 狀態碼"):
            # 驗證伺服器有如期回報 404
            assert response.status_code == 404, f"預期收到 404 Not Found，但收到 {response.status_code}"
            print(f"\n【GET 異常情境成功】查無此 ID 時，系統如期回傳 404 錯誤碼")

    # POST 新增資源
    @allure.story("POST 請求 - 新增資源 (POST /posts)")
    def test_create_post(self, api_session):
        """
        【測試目的】驗證能否成功傳送 JSON Payload 建立一筆新文章。
        """
        # 資料準備：建立一個新的文章內容
        payload = {
            "title": "自動化測試練習文章",
            "body": "這是一篇透過 pytest 與 requests 函式庫發送 POST 請求建立的測試資料。",
            "userId": 1
        }

        with allure.step("步驟 1：發送 POST 請求新增文章"):
            # 使用 post 方法，傳入 json 參數
            response = api_session.post(f"{BASE_URL}/posts", json=payload, timeout=10)

        with allure.step("步驟 2：驗證新增結果 (狀態碼 201 與回傳內容)"):
            # HTTP 201 代表 Created (資源已成功建立)
            assert response.status_code == 201, f"預期狀態碼 201，但收到 {response.status_code}"
            result = response.json()
            
            # 伺服器成功建立後為新資源配發唯一的 ID
            assert "id" in result, "新增成功後，伺服器應回傳新建立的 id 欄位"
            
            # 驗證回傳的內容是否與當初送出的 json 內容一致
            assert result["title"] == payload["title"], "回傳標題與送出標題不符"
            assert result["body"] == payload["body"], "回傳內文與送出內文不符"
            assert result["userId"] == payload["userId"], "回傳 userId 與送出 userId 不符"
            
            print(f"\n【POST 成功】文章新增成功！伺服器配發的 ID 為: {result['id']}")

    # PUT 完整更新資源
    @allure.story("PUT 請求 - 完整更新既有資源 (PUT /posts/{id})")
    def test_update_post(self, api_session):
        """
        【測試目的】驗證能否完整覆蓋更新已存在的文章內容。
            驗證狀態碼 200 及回傳的欄位是否已更新為新值。
          * PUT 用於「完整替換」整筆資料（所有必填欄位都要帶）。
          * PATCH 用於「部分修改」（只需帶想更新的單一欄位）。
        
        """
        post_id = 1
        # 準備要更新的新資料 (包含 ID、新標題、新內文)
        payload = {
            "id": post_id,
            "title": "已成功更新的文章標題 (PUT)",
            "body": "這篇文章的內容已經透過 PUT 請求被自動化更新完畢。",
            "userId": 1
        }

        with allure.step(f"步驟 1：發送 PUT 請求更新 ID={post_id} 的文章"):
            response = api_session.put(f"{BASE_URL}/posts/{post_id}", json=payload, timeout=10)

        with allure.step("步驟 2：驗證更新結果"):
            # 更新成功回傳 200
            assert response.status_code == 200, f"更新失敗，狀態碼為: {response.status_code}"
            result = response.json()
            
            # 驗證回傳的資料確實變成設定的新標題
            assert result["title"] == payload["title"], "更新後的標題不正確"
            assert result["id"] == post_id, "更新後回傳的 ID 與原 ID 不符"
            print(f"\n【PUT 成功】文章 ID={post_id} 更新完成，新標題為: {result['title']}")

    # DELETE 刪除資源
    @allure.story("DELETE 請求 - 刪除資源 (DELETE /posts/{id})")
    def test_delete_post(self, api_session):
        """
        【測試目的】驗證發送 DELETE 請求刪除指定 ID 的文章。
            - DELETE 請求通常不需要 Body，只需指定目標路徑。
            - 回傳狀態碼有 200 (含回傳訊息) 或 204 No Content (無回傳內容)。
        """
        post_id = 1
        with allure.step(f"步驟 1：發送 DELETE 請求刪除 ID={post_id} 的文章"):
            response = api_session.delete(f"{BASE_URL}/posts/{post_id}", timeout=10)

        with allure.step("步驟 2：驗證刪除結果"):
            # JSONPlaceholder 在刪除成功時會回傳 200 OK (回傳空物件 {})
            assert response.status_code == 200, f"刪除失敗，收到狀態碼: {response.status_code}"
            print(f"\n【DELETE 成功】文章 ID={post_id} 已成功發送刪除請求，伺服器回傳狀態碼: {response.status_code}")
