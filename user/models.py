from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify


class Profile(models.Model):
    id = models.UUIDField(primary_key = True, unique = True, db_index = True, default = uuid.uuid4, editable = False)
    user = models.OneToOneField(User, on_delete = models.CASCADE) # request.user.profile
    name = models.CharField(max_length = 150, verbose_name = 'İsim Soyisim')
    bio = models.TextField(max_length = 300, verbose_name = 'Hakkımda', default = 'Merhaba Ben Twitter kullanıyorum')
    image = models.ImageField(upload_to= 'profiles/', verbose_name = 'Profil Resmi') #imagefield kullanabilmemiz için : pip install Pillow
    follow = models.ManyToManyField('self', symmetrical=False, related_name='takip', verbose_name = 'Takip Edilenler', blank= True)
    follower = models.ManyToManyField('self', symmetrical=False, related_name='takipçi', verbose_name = 'Takipçiler', blank = True)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Katılma Tarihi')
    slug = models.SlugField(blank = True, null = True, editable=False)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Profiller'
        verbose_name = 'Profil'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username.replace('ı','i'))
        super().save(*args, **kwargs)