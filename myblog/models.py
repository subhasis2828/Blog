from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Blogs(models.Model):
    id=models.AutoField(primary_key=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title  = models.CharField(max_length=256)
    decs = models.TextField()
    image = models.ImageField(upload_to = "Blog_image")
    created_at = models.DateTimeField(auto_now=True)    
    updated_at = models.DateTimeField(auto_now=True)