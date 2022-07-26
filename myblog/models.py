from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
# Create your models here.
class Blogs(models.Model):
    id=models.AutoField(primary_key=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title  = models.CharField(max_length=256)
    decs = models.TextField()
    image = models.ImageField(upload_to = "Blog_image")
    created_at = models.DateTimeField(auto_now=True)    
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User,related_name="likes")
    dislike = models.ManyToManyField(User,related_name="dislike")

    def total_like(self,  *args, **kwargs):
        return self.like.all().count()
    def total_dislike(self,  *args, **kwargs):
        return self.dislike.all().count()


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    blog = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)    
    updated_at = models.DateTimeField(auto_now=True)