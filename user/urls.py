from django.urls import path
from .views import *

urlpatterns = [
    path('kayit-giris/', loginRegister, name = 'login'),
    path('cikis/', userLogout, name='logout'),
    path('profil/<str:slug>', profile, name='profile'),
    path('back/', back, name="back"),
    path('duzenle/', change, name = 'change'),
    path('yer-isaretleri/', savedTweets, name = 'saves')
]
