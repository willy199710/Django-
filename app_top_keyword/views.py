from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def home(request):
    return render(request, 'app_top_keyword/home.html')

print("app_top_keywords--類別熱門關鍵字載入成功!")

