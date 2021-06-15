from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render

def load_data_pk():
    # Read data from csv file
    df_pk = pd.read_csv('app_leaderboard/dataset/pk_politician.csv',sep='|')
    
    global koaTsaiHan
    koaTsaiHan = dict(list(df_pk.values))

    df_pk = pd.read_csv('app_leaderboard/dataset/pk_political_party.csv',sep='|')

    global kmtDppTpp
    kmtDppTpp = dict(list(df_pk.values))
    del df_pk

# load pk data
load_data_pk()

def pk_politician(request):
    return render(request,'app_leaderboard/pk_politics.html', koaTsaiHan)

def pk_political_party(request):
    return render(request,'app_leaderboard/pk_politics.html', kmtDppTpp)
print('app_leaderboard was loaded!')
