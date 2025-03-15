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

@csrf_exempt
def voice(request):
    if request.method == 'POST':
        try:
            # 解析前端發送的 JSON 數據
            data = json.loads(request.body)
            voice_input = data.get('voice_input')

            # 在這裡，你可以對語音輸入進行進一步處理

            # 回傳處理後的結果，這裡渲染一個模板，並傳遞處理後的數據
            return render(request, 'voice.html', {'message': 'Received input: ' + voice_input})
        except json.JSONDecodeError:
            return render(request, 'voice.html', {'error': 'Invalid JSON'})
    else:
        return render(request, 'voice.html', {'error': 'Invalid request method'})

