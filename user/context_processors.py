from .models import *
import random

def get_profiles(request):
    profiles_follows = ""
    if request.user.is_authenticated:
        myProfil = request.user.profile
        myFollows = myProfil.follow.all() #bizim takip ettiklerimiz
        profiles_follows = Profile.objects.filter(follower__in = myFollows).exclude(follower__in = [myProfil]).exclude(name = myProfil.name).distinct()
        profiles_list = list(profiles_follows)
        random.shuffle(profiles_list) #listenin içerisindeki elemanların sırasını karıştırma işlemi
        profiles_follows = profiles_list[:5]

    return {'profiles_follows':profiles_follows}