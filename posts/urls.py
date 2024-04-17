from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('tweet/<str:postId>', comment, name= "comment"),
    path('kesfet/', explore, name='explore'),
    path('arama/', search, name = "search"),
    path('bildirimler/', notifications, name='notifications')
]
