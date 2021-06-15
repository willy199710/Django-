from django.urls import path
from app_leaderboard import views

app_name='namespace_leaderboard'

urlpatterns = [
    path('', views.pk_politician, name='politician'),
    path('politicalparty', views.pk_political_party, name='politicalParty'),
]

