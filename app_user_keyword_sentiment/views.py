from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from datetime import datetime, timedelta


# (1) Load news data--approach 1
# df = pd.read_csv('dataset/news_dataset_preprocessed_for_django.csv',sep='|')

# (2) Load news data--approach 2
def load_df_data_v1():
    global df # global variable
    #df = pd.read_csv('dataset/news_dataset_preprocessed_for_django.csv',sep='|')
    df = pd.read_csv('app_userkey_sentiment/dataset/news_dataset_preprocessed_for_django.csv',sep='|')

# (3) Load news data--approach 3
# We can use df from the app_user_keyword
# from app_user_keyword.views import df

# (4) Load news data--approach 4
# import from app_user_keyword.views and use df later
import app_user_keyword.views as userkeyword_views
def load_df_data():
    # import and use df from app_user_keyword 
    global df # global variable
    df = userkeyword_views.df

# call load data function when starting server
load_df_data()


def home(request):
    return render(request, 'app_user_keyword_sentiment/home.html')

def api_get_userkey_sentiment(request):

    userkey = request.GET['userkey']
    cate = request.GET['cate']
    cond = request.GET['cond']
    weeks = int(request.GET['weeks'])

    key = userkey.split()

    # global variable
    # global  df_query

    # Proceed filtering
    df_query = filter_dataFrame_fullText(key, cond, cate, weeks)
    print(key)
    print(len(df_query))
    

    sentiCount, sentiPercnt = get_article_sentiment(df_query)

    if weeks <= 4:
        freq_type = 'D'
    else:
        freq_type = 'W'

    data_pos, data_neg = get_key_time_based_sentiment( df_query, freq_type )

    response = {
        'sentiCount': sentiCount,
        'data_pos':data_pos,
        'data_neg':data_neg,
    }
    return JsonResponse(response)

def get_article_sentiment(df_query):
    sentiCount = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    sentiPercnt = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    numberOfArticle = len(df_query)
    for senti in df_query.sentiment:
        # determine sentimental polarity
        if float(senti) >= 0.75:
            sentiCount['Positive'] += 1
        elif float(senti) <= 0.4:
            sentiCount['Negative'] += 1
        else:
            sentiCount['Neutral'] += 1
    for polar in sentiCount :
        sentiPercnt[polar]=int(sentiCount[polar]/numberOfArticle*100)
        #sentiPercnt[polar]=round(sentiCount[polar]/numberOfArticle,2)
    return sentiCount, sentiPercnt


def get_key_time_based_sentiment(df_query, freq_type='D'):

    # date samples
    date_samples = df_query.date

    # positive
    pos_freq = pd.DataFrame({'date_index': pd.to_datetime(date_samples),
                             'pos': [(lambda x: 1 if x >= 0.6 else 0)(s) for s in df_query.sentiment]})
    data = pos_freq.groupby(pd.Grouper(key='date_index', freq= freq_type)).sum()
    data_pos = []
    for i, idx in enumerate(data.index):
        row = {'x': idx.strftime('%Y-%m-%d'), 'y': int(data.iloc[i].pos)}
        data_pos.append(row)

    # negative
    neg_freq = pd.DataFrame({'date_index': pd.to_datetime(date_samples),
                             'neg': [(lambda x: 1 if x <= 0.4 else 0)(s) for s in df_query.sentiment]})
    data = neg_freq.groupby(pd.Grouper(key='date_index', freq= freq_type)).sum()
    data_neg = []
    for i, idx in enumerate(data.index):
        row = {'x': idx.strftime('%Y-%m-%d'), 'y': int(data.iloc[i].neg)}
        data_neg.append(row)

    return data_pos, data_neg

def filter_dataFrame_fullText(user_keywords, cond, cate,weeks):

    # end date: the date of the latest record of news
    end_date = df.date.max()
    
    # start date
    start_date = (datetime.strptime(end_date, '%Y-%m-%d').date() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')

    # proceed filtering
    if (cate == "全部") & (cond == 'and'):
        df_query = df[(df.date >= start_date) & (df.date <= end_date) & df.content.apply(
            lambda row: all((qk in row) for qk in user_keywords))]
    elif (cate == "全部") & (cond == 'or'):
        queryKey = '|'.join(user_keywords)
        df_query = df[(df['date'] >= start_date) & (df['date'] <= end_date) & df.content.str.contains(queryKey)]
    elif (cond == 'and'):
        df_query = df[(df.category == cate) & (df.date >= start_date) & (df.date <= end_date) & df.content.apply(
            lambda row: all((qk in row) for qk in user_keywords))]
    elif (cond == 'or'):
        queryKey = '|'.join(user_keywords)
        df_query = df[(df.category == cate) & (df['date'] >= start_date) & (df['date'] <= end_date) & df[
            'content'].str.contains(queryKey)]

    return df_query

print("app_userkey_sentiment was loaded!")
