from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='pricetracker_home'),
    path('save_tracklist/', views.save_tracklist, name='save_tracklist'),
    path('checknow/', views.checknow, name='checknow'),
    path('send_email/', views.send_email, name='send_test_email'),
]
