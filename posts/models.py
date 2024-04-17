from django.db import models
import uuid
from django.core.mail import send_mail
from django.conf import settings

class Post(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, db_index = True, default =  uuid.uuid4, editable= False)
    author = models.ForeignKey('user.Profile', on_delete = models.CASCADE, verbose_name = 'Yazar')
    content = models.TextField(max_length = 200, verbose_name = 'Tweet')
    like = models.ManyToManyField('user.Profile', related_name= 'likes', verbose_name= 'Beğenenler')
    saves = models.ManyToManyField('user.Profile', related_name= 'saves', verbose_name= 'Kaydedenler')
    retweet = models.ManyToManyField('user.Profile', related_name= 'retweets', verbose_name= 'Retweet edenler')
    view = models.ManyToManyField('user.Profile', related_name= 'views', verbose_name= 'Görüntüleyenler')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Oluşturulma Tarihi')
    slug = models.SlugField(blank = True, null = True, editable = False)


    def __str__(self):
        return self.author.name
    class Meta:
        verbose_name_plural = 'Tweetler'
        verbose_name = 'Tweet'
        ordering = ['-created_at']

class Comment(models.Model):
    owner = models.ForeignKey('user.Profile', on_delete= models.CASCADE, verbose_name = 'Yorum yapan')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name = 'Yorum yapılan Tweet')
    content = models.TextField(max_length=200, verbose_name = 'Yorum')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.content
    
    class Meta:
        verbose_name_plural = 'Yorumlar'
        verbose_name = 'Yorum'

class Notificate(models.Model):
    ACTIONS = (
        ('begeni', 'Beğeni'),
        ('retweet', 'Retweet'),
        ('yorum', 'Yorum'),
        ('takip', 'Takip')
    )
    receiver = models.ForeignKey('user.Profile', on_delete = models.CASCADE, verbose_name = 'Bildirim Alan')
    sender = models.ForeignKey('user.Profile', related_name = 'gonderen', on_delete = models.CASCADE, verbose_name = 'Bildirim Gönderen/İşlem Yapan')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name = 'İşlem Yapılan Post', blank = True, null = True)
    message = models.TextField(('İşlem Mesajı'))
    islem = models.CharField(max_length = 100, choices = ACTIONS, verbose_name = 'İşlem')
    isRead = models.BooleanField(default = False, verbose_name = 'Okundu Bilgisi')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'işlem Yapılan Tarih')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        count = Notificate.objects.filter(receiver = self.receiver, isRead = False).count()
        if count == 5 or count == 10 :
            subject = "Yeni bildirimleriniz var"
            message = "Hesabınızda yeni bildirimler mevcut. Hesabınıza giriş yapıp bildirimler sayfasından kontrol edebilirsiniz"
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [self.receiver.user.email],
                fail_silently = False
            )


    def __str__(self):
        return self.receiver.name
    
    class Meta:
        verbose_name_plural = 'Bildirimler'
        verbose_name = 'Bildirim'