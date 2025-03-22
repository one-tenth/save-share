from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("hello world")

#--------------------------------------
#ocr
import os
import io
from django.http import JsonResponse
from google.cloud import vision
from django.conf import settings

# 設定 Google API 憑證
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(settings.BASE_DIR, "service-account.json")

def extract_text_from_image(image_file):
    """ 使用 Google Cloud Vision API 解析圖片中的文字（不儲存檔案） """
    client = vision.ImageAnnotatorClient()
    
    # 讀取記憶體中的圖片
    content = image_file.read()
    image = vision.Image(content=content)
    
    response = client.text_detection(image=image)
    texts = response.text_annotations

    return texts[0].description.strip() if texts else ""

def ocr(request):
    """ 直接處理圖片並解析文字，不儲存 """
    if request.method == "POST" and request.FILES.get("image"):
        uploaded_file = request.FILES["image"]

        # 直接從記憶體處理圖片
        extracted_text = extract_text_from_image(uploaded_file)

        return JsonResponse({"text": extracted_text})
    return render(request,'ocr.html')
    return JsonResponse({"error": "無效的請求"}, status=400)
