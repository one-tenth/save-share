from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("hello world")


#---------------------------------------------------------------
#語音
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import jieba

@csrf_exempt
def voice_page(request):#讓json有網頁可以回傳
    return render(request,'voice.html')


@csrf_exempt
def voice(request):
    if request.method == 'POST':
        try:
            # 解析前端發送的 JSON 數據
            data = json.loads(request.body)
            voice_input = data.get('voice_input', '').strip()

            if not voice_input:
                return JsonResponse({'error': '語音輸入為空'}, status=400)

            # 使用 jieba 進行分詞
            keywords = list(jieba.cut(voice_input))

            # 合併數字與單位
            combined_keywords = []
            skip_next = False
            for i, word in enumerate(keywords):
                if skip_next:
                    skip_next = False
                    continue
                if word.isdigit() and i + 1 < len(keywords) and keywords[i + 1] in ['萬', '元']:
                    combined_keywords.append(word + keywords[i + 1])  # 合併數字與單位
                    skip_next = True
                elif word.isdigit() and len(word) >= 6:  # 處理「1000000」的情況
                    combined_keywords.append(f"{int(word) // 10000}萬")
                else:
                    combined_keywords.append(word)

            print("分詞結果（合併數字與單位）:", combined_keywords)

            # 自訂關鍵字分類邏輯
            categories = {
                '金融': ['投資', '股票', '銀行', '基金'],
                '科技': ['人工智慧', '電腦', '程式', '網路'],
                '生活': ['天氣', '飲食', '健康', '運動']
            }

            classified_category = "未知"
            for category, words in categories.items():
                if any(word in combined_keywords for word in words):
                    classified_category = category
                    break

            return JsonResponse({
                'message': f'接收到的語音內容: {voice_input}',
                'keywords': keywords,
                'category': classified_category
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': '無效的 JSON'}, status=400)

    return JsonResponse({'error': '請使用 POST 方法發送請求'}, status=405)


