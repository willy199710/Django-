"""website_configs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

urlpatterns = [
    # top keywords
    path('topword/', include('app_top_keyword.urls')),
    path('topperson/', include('app_top_person.urls')),
    path('topner/', include('app_top_ner.urls')),
    path('userkeyword/', include('app_user_keyword.urls')),
    path('userkeyword_assoc/', include('app_user_keyword_association.urls')),
    path('userkeyword_senti/', include('app_user_keyword_sentiment.urls')),
    path('news_rcmd/', include('app_news_rcmd.urls')),
    # leaderboard
    path('politicalPK/', include('app_leaderboard.urls')),
    # course introduction
    path('introduction', TemplateView.as_view(template_name='introduction.html'), name='course_introduction'),
    path('delicious', TemplateView.as_view(template_name='delicious.html'), name='course_delicious')


]

