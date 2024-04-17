from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.db.models import Q
from user.models import *

def userActions(request):
    profile = request.user.profile
    postId = request.POST.get('postId')
    post = Post.objects.get(id=postId)
    post.view.add(profile)
    yeniBildirim = Notificate(
        receiver = post.author,
        sender = profile,
        post = post
    )
    if 'retweet' in request.POST:
        if profile in post.retweet.all():
            post.retweet.remove(profile)
        else:
            post.retweet.add(profile)
            yeniBildirim.islem = 'retweet'
            yeniBildirim.message = f"{yeniBildirim.sender.name} kullanıcı '{yeniBildirim.post.content}' gönderinizi retweet etti."
            yeniBildirim.save()
        post.save
        
    if 'like' in request.POST:
        if profile in post.like.all():
            post.like.remove(profile)
        else:
            post.like.add(profile)
            yeniBildirim.islem = 'begeni'
            yeniBildirim.message = f"{yeniBildirim.sender.name} kullanıcı '{yeniBildirim.post.content}' gönderinizi beğendi."
            yeniBildirim.save()
        post.save()
        
    if 'save' in request.POST:
        if profile in post.saves.all():
            post.saves.remove(profile)
        else:
            post.saves.add(profile)
        post.save()
@login_required(login_url='login')

def index(request):
    # follows = request.user.profile.follow.all()
    # posts = Post.objects.filter(author = [follows])
    posts = Post.objects.all()
    if request.method == 'POST':
        profile = request.user.profile
        if 'tweet' in request.POST:
            post = request.POST.get('postForm')
            newPost = Post.objects.create(
                author = profile,
                content = post
            )
            newPost.save()
            messages.success(request, 'Tweetiniz yayınlandı')
            return redirect('index')
        else:

            userActions(request)
            return redirect('index')
    context = {
        'posts':posts
    }
    return render(request, 'index.html', context)

def comment(request, postId):
    post = Post.objects.get(id=postId)
    post.view.add(request.user.profile)
    if request.method == "POST":
        if 'commentButton' in request.POST:
            commentForm = request.POST.get('commentForm')
            newComment = Comment.objects.create(
                owner = request.user.profile,
                post = post,
                content = commentForm
            )
            newComment.save()
            yeniBildirim = Notificate(
                receiver = post.author,
                sender = request.user.profile,
                post = post,
                islem = 'yorum',
                message  = f"{request.user.profile} kullanıcısı '{post.content}' gönderinize yorum yaptı <br>Yorumu: {commentForm}"
            )
            yeniBildirim.save()
            messages.success(request, 'Yorumunuz yayınlandı')
            return redirect('comment', postId = post.id)
        else:
            userActions(request)
            return redirect('comment', postId = post.id)
    context = {
        'post':post
    }
    return render(request, 'comment.html', context)

def explore(request):
    posts = Post.objects.all().order_by('?')
    if request.method == 'POST':
        userActions(request)
    context = {
        'posts':posts
    }
    return render(request, 'explore.html', context)

def search(request):
    profiles = ""
    posts = ""
    query = ""
    if request.GET.get('q'):
        query = request.GET.get('q')
        if '@' in query:
            queryP = query[1:] #@gokhan -> gokhan
            profiles = Profile.objects.filter(
                Q(name__icontains = queryP) |
                Q(user__username__icontains = queryP)
            ).distinct()
        else:
            posts = Post.objects.filter(content__icontains = query)
    if request.method == 'POST':
        userActions(request)
    context = {
        'profiles':profiles,
        'posts':posts,
        'query':query
    }
    return render(request, 'search.html', context)

def notifications(request):
    bildirimler = Notificate.objects.filter(receiver = request.user.profile)
    if request.method == 'POST':
        for bildirim in bildirimler.filter(isRead = False): #sadece okunmamış olduğumuz bildirimleri çektik.
            bildirim.isRead = True
            bildirim.save()
        return redirect('notifications')

    context = {
        'bildirimler':bildirimler
    }
    return render(request, 'notifications.html', context)