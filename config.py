import os
from pathlib import Path
# 讀取 .env 檔工具
from dotenv import load_dotenv

# 讀取 .env 檔案中的環境變數
load_dotenv()

class Config:
    # 抓取 config.py 所在的目錄
    ROOT_DIR = Path(__file__).resolve().parent
    
    IMAGE_DIR = ROOT_DIR / "images"
    
    TARGET_URL = os.getenv("SAUCE_URL")
    USERNAME = os.getenv("SAUCE_USERNAME")
    PASSWORD = os.getenv("SAUCE_PASSWORD")
    
    # 全域等待秒數
    TIMEOUT = 10