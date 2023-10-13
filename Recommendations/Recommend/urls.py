from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.recommend, name='recommend'),
     path('', views.index, name='index'),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('<int:food_id>/', views.detail, name='review'),
    path('watch/', views.watch, name='watch'),

]