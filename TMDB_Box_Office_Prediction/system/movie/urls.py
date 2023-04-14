from django.urls import path
from movie.views import index,filechoose
app_name = 'Search'

urlpatterns = [
    path('', index, name='boxoffice'),
    path('file/', filechoose, name='filechoose'),
]
