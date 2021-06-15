from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from datetime import datetime, timedelta
import pandas as pd
import math
import re
from collections import Counter
# (1) we can load data using read_csv()
# global variable
# df = pd.read_csv('dataset/cna_news_200_preprocessed.csv', sep='|')


# (2) we can load data using reload_df_data() function
def load_df_data_v1():
    # global variable
    global  df
    df = pd.read_csv('app_user_keyword/dataset/cna_news_200_preprocessed.csv', sep='|')

# (3) df can be import from app_user_keyword
# To save memory, we just import df from the other app as follows.
# from app_user_keyword.views import df

# (4) df can be import from app_user_keyword
import app_user_keyword.views as userkeyword_views
def load_df_data():
    # import and use df from app_user_keyword 
    global df # global variable
    df = userkeyword_views.df

load_df_data()

# For the key association analysis
def home(request):
    return render(request, 'app_user_keyword_association/home.html')

# df_query should be global
@csrf_exempt
def api_get_userkey_associate(request):

    userkey = request.POST.get('userkey')
    cate = request.POST['cate'] # This is an alternative way to get POST data.
    cond = request.POST.get('cond')
    weeks = int(request.POST.get('weeks'))
    key = userkey.split()

    global  df_query # global variable

    df_query = filter_dataFrame_fullText(key, cond, cate,weeks)
    print(key)
    print(len(df_query))

    if len(df_query) != 0:  # df_query is not empty
        newslinks = get_title_link_top10()
        related_words, clouddata = get_related_words(key)
        same_paragraph = get_same_para(key,cond) # multiple keywords
        same_paragraph_top10 = same_paragraph[0: 10]

    else:
        newslinks = []
        related_words = []
        same_paragraph_top10 = []
        clouddata = []

    response = {
        'newslinks': newslinks,
        'related_words': related_words,
        'same_paragraph': same_paragraph_top10,
        'clouddata':clouddata,
    }
    return JsonResponse(response)


def filter_dataFrame_fullText(key, cond, cate,weeks):

    # end date: the date of the last record of news
    end_date = df.date.max()
    print('latest date for dataset:', end_date)

    # start date
    start_date = (datetime.strptime(end_date, '%Y-%m-%d').date() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')

    # filtering
    if (cate == "全部") & (cond == 'and'):
        query_df = df[(df.date >= start_date) & (df.date <= end_date) & df.content.apply(
            lambda row: all((qk in row) for qk in key))]
    elif (cate == "全部") & (cond == 'or'):
        queryKey = '|'.join(key)
        query_df = df[(df['date'] >= start_date) & (df['date'] <= end_date) & df.content.str.contains(queryKey)]
    elif (cond == 'and'):
        query_df = df[(df.category == cate) & (df.date >= start_date) & (df.date <= end_date) & df.content.apply(
            lambda row: all((qk in row) for qk in key))]
    elif (cond == 'or'):
        queryKey = '|'.join(key)
        query_df = df[(df.category == cate) & (df['date'] >= start_date) & (df['date'] <= end_date) & df[
            'content'].str.contains(queryKey)]

    return query_df

# get 10 titles and links
def get_title_link_top10():
    items = []
    for i in range( len(df_query[0:10]) ): # show only 10 news
        category = df_query.iloc[i]['category']
        title = df_query.iloc[i]['title']
        link = df_query.iloc[i]['link']
        photo_link = df_query.iloc[i]['photo_link']
        # if photo_link value is NaN, replace it with empty string 
        if pd.isna(photo_link):
            photo_link=''
        
        item_info = {
            'category': category, 
            'title': title, 
            'link': link, 
            'photo_link': photo_link
        }

        items.append(item_info)
    return items 

# Get related keywords by counting the top keywords of each news.
# Notice:  do not name function as  "get_related_keys",
# because this name is used in Django
def get_related_words(key):

    # df_query = df[df['tokens'].str.contains(query_key)]
    all_pairs = {}
    for idx in range(len(df_query)):
        row = df_query.iloc[idx].top_keys_freq # column name may be top_keys_freq
        pairs = dict(eval(row))

        # Get related keywords by counting the top keywords of each news.
        for pair in pairs.items():
            w, f = pair
            if w in all_pairs:
                all_pairs[w] += f
            else:
                all_pairs[w] = f
    counter = Counter(all_pairs)

    wf_pairs = counter.most_common(30)

    # cloud chart data
    # the minimum and maximum frequency of top words
    min_ = wf_pairs[-1][1]  # the last line is smaller
    max_ = wf_pairs[0][1]
    # text size based on the value of word frequency for drawing cloud chart
    textSizeMin = 20
    textSizeMax = 120

    clouddata = [{'text': w, 'size': int(textSizeMin + (f - min_) / (max_ - min_) * (textSizeMax - textSizeMin))}
                 for w, f in wf_pairs]

    return   wf_pairs, clouddata 

# split paragraphs
def cut_paragraph(text):
    result = re.split('[。|！|\!|？|\?]', text)
    result = list(filter(None, result))
    return result

# Find out all paragraphs where multiple keywords occur.
def get_same_para( key, cond):
    same_para=[]
    for text in df_query.content:
        #print(text)
        paragraphs = cut_paragraph(text)
        for para in paragraphs:
            para += "。"
            if cond=='and':
                if all([re.search(kw, para) for kw in key]):
                    same_para.append(para)
            elif cond=='or':
                if any([re.search(kw, para) for kw in key]):
                    same_para.append(para)
    return same_para
print("app_user_keyword_association was loaded!")
