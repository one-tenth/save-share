import os
import io
from google.cloud import vision

# 獲取專案的根目錄
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_google_ocr(image_filename):
    """ 測試 Google OCR API """
    client = vision.ImageAnnotatorClient()

    # 取得圖片的絕對路徑
    image_path = os.path.join(BASE_DIR, 'static', image_filename)

    # 確保檔案存在
    if not os.path.exists(image_path):
        print(f"❌ 檔案不存在：{image_path}")
        return

    with io.open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        print("✅ OCR 讀取結果:")
        print(texts[0].description)
    else:
        print("❌ 沒有讀取到文字")

# 測試 OCR
test_google_ocr("IMG_1026.JPG")
