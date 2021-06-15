from django.urls import path
from app_user_keyword_sentiment import views

app_name="namespace_userkey_sentiment"

urlpatterns = [
    # For the user userkey sentiment analysis page
    path('', views.home, name='home'),
    path('api_get_userkey_sentiment/', views.api_get_userkey_sentiment),
]
