from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Post Modeli (Postlar dizimi)
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts', verbose_name="Kategoriya", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', null=True, blank=True, related_name='posts', verbose_name='tag')


    def __str__(self):
        return self.title
    
# Teglar 
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='teg')
    def __str__(self):
        return self.name


# Kommentariyalar

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Kommentariya', related_name='comments')
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentss', verbose_name='Kommentariya Avtori')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} user writed comment in {self.post}"
    


# Kategoriyalar
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)



class Info(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)

