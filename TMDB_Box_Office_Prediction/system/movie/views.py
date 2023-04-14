import os
import time
import codecs
import csv
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from joblib import load
import numpy as np
# Create your views here.
def index(request):
    data = dict()
    data['collection'] = '1'
    data['has_homepage'] = '1'
    data['is_en'] = '1'
    data['has_tagline'] = '1'
    if request.method == 'POST':
        moviename = request.POST['moviename']
        budget = request.POST['budget']
        log_budget = np.log1p(int(budget))
        popularity = request.POST['popularity']
        runtime = request.POST['runtime']
        collection = request.POST['collection']
        has_homepage = request.POST['has_homepage']
        is_en = request.POST['is_en']
        has_tagline = request.POST['has_tagline']
        num_production_companies = request.POST['num_production_companies']
        num_production_countries = request.POST['num_production_countries']
        num_spoken_languages = request.POST['num_spoken_languages']
        num_Keywords = request.POST['num_Keywords']
        num_cast = request.POST['num_cast']
        num_crew = request.POST['num_crew']
        is_popular_genres = request.POST['is_popular_genres']
        if (int(is_popular_genres) > 6):
            is_popular_genres = 6
        release_date = request.POST['first_date']
        release_year = datetime.strptime(release_date, '%Y-%m-%d').strftime('%Y')
        release_day = int(datetime.strptime(release_date, '%Y-%m-%d').strftime('%d'))
        release_month = int(datetime.strptime(release_date, '%Y-%m-%d').strftime('%m'))
        print(log_budget, popularity, runtime, collection, has_homepage, is_en, has_tagline, num_production_companies,
              num_production_countries,num_spoken_languages,num_Keywords,num_cast,num_crew,is_popular_genres, release_date, release_month,release_year,release_day)
        input_data = [[log_budget, popularity, runtime, collection, has_homepage, is_en, has_tagline, num_production_companies, num_production_countries,
                       num_spoken_languages,num_Keywords,num_cast,num_crew,is_popular_genres,release_year, release_day, release_month]]
        end = time.time()
        # 加载训练好的随机森林模型
        model = load('trained_model.pkl')
        predicted_result = np.expm1(model.predict(input_data))
        usetime = time.time()-end
        data['predicted_result'] = predicted_result
        data['budget'] = budget
        data['popularity'] = popularity
        data['runtime'] = runtime
        data['collection'] = collection
        data['has_homepage'] = has_homepage
        data['is_en'] = is_en
        data['has_tagline'] = has_tagline
        data['num_production_companies'] = num_production_companies
        data['num_production_countries'] = num_production_countries
        data['num_spoken_languages'] = num_spoken_languages
        data['num_Keywords'] = num_Keywords
        data['num_cast'] = num_cast
        data['num_crew'] = num_crew
        data['is_popular_genres'] = is_popular_genres
        data['first_date'] = release_date
        data['moviename'] = moviename
        data['usetime'] = usetime
    return render(request, 'index.html', data)

def filechoose(request):
    data = dict()
    if request.method == 'POST':
        dir = request.FILES
        filename = request.FILES['formFile'].name
        data['filename'] = filename
        MEDIA_ROOT='D:\BoxOffice\movie\static'
        storefilename = os.path.join(MEDIA_ROOT, filename)
        with open(storefilename, 'wb') as f:
            for i in request.FILES['formFile'].chunks():
                f.write(i)
        result = []
        with open(storefilename, encoding='utf-8-sig') as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            end = time.time()
            for row in f_csv:
                start = time.time()
                budget = row[1]
                log_budget = np.log1p(int(budget))
                input_data = [[log_budget, row[2], row[3], row[5], row[6], row[7], row[8],
                               row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16],
                               row[17], row[18]]]
                # 加载训练好的随机森林模型
                model = load('trained_model.pkl')
                predicted_result = np.expm1(model.predict(input_data))
                usetime = time.time() - start
                r = {
                    'id': row[0],
                    'renvenue': predicted_result,
                    'usetime': usetime
                }
                result.append(r)
            usetime = time.time() - end
        data['results'] = result
        data['totaltime'] = usetime
        os.remove(storefilename)
    return render(request, 'file.html', data)
