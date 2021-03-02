from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('account/', views.account, name='account'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, 
                                                         name='post_detail'),
    path('mlposts/', views.most_liked, name='mlposts'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/mlcomments/', views.most_liked_comments, name='mlcomments'),
    path('create/', views.create_post, name='create'),
    path('mystories/', views.my_stories, name='my_stories'),
    path('mycomments/', views.my_comments, name='my_comments'),
    path('drafted/', views.drafted, name='drafted'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/postedit/', views.post_edit, name='post_edit'),
    path('test/', views.test, name='test')
]