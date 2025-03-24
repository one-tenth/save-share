from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("hello world")

#--------------------------------------
#ocr   
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from google.cloud import vision

# 設定 Google 憑證（也可搬去 settings.py 統一管理）
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(settings.BASE_DIR, "google-credentials.json")

# 顯示前端頁面
def show_ocr_page(request):
    return render(request, 'ocr.html')

# 接收圖片進行辨識
@csrf_exempt
def ocr(request):
    if request.method == "POST" and request.FILES.get("image"):
        image_file = request.FILES["image"]

        try:
            client = vision.ImageAnnotatorClient()
            image = vision.Image(content=image_file.read())
            response = client.text_detection(image=image)
            texts = response.text_annotations

            if texts:
                return JsonResponse({"text": texts[0].description.strip()})
            else:
                return JsonResponse({"text": "❌ 沒有讀取到任何文字"})

        except Exception as e:
            return JsonResponse({"text": f"❌ 發生錯誤：{str(e)}"})

    return JsonResponse({"error": "❌ 無效的請求，請使用 POST 並附上 image"}, status=400)

