from datetime import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from myblog.models import Blogs
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as UserLogin
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    recent_blogs = Blogs.objects.all().order_by("-updated_at")[:3]
    best_blogs = Blogs.objects.all().exclude(id__in = recent_blogs.values('id')).order_by("?")[:2]
    context={
        "recent_blogs":recent_blogs,
        "best_blogs":best_blogs

    }
    return render(request,'index.html',context)

def Signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('yourblog'))
    if request.method=='POST':
        username= request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            UserLogin(request,user)
            messages.success(request, 'User Crerated')
            return HttpResponseRedirect(reverse('addblog'))
        else:
            messages.error(request, 'Confirm Password not matched')
            return redirect('login')
    else:
        return redirect('login')
    

def Login(request):
    if request.user.is_authenticated:
        return redirect('yourblog')
    if request.method == 'POST':
        print("beefoe auth")
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("beefoe auth")
        user = authenticate(username=username,password=password)
        print("user is",user)
        if user is not None:
            UserLogin(request,user)
            return HttpResponseRedirect(reverse('addblog'))
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request,'login.html')

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def Allblog(request):
    blogs = Blogs.objects.all().order_by("-created_at")
    return render(request,'blogs.html',{"blogs":blogs})

def Blog(request,id):
    blog = Blogs.objects.get(id = id)
    blogs = Blogs.objects.all().exclude(id=id).order_by("?")[:5]
    return render(request,'blog.html',{"blogs":blogs,"blog":blog})

@login_required
def AddBlog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        if title and desc and image:
            blog = Blogs(title = title,decs =  desc,image = image,author = request.user)
            blog.save()
            messages.success(request, 'Blog created')
            return HttpResponseRedirect(reverse('addblog'))
        else:
            messages.error(request, 'Please Fill All the fileds')
            return HttpResponseRedirect(reverse('addblog'))
    else:
        return render(request,'addblog.html')


@login_required
def YourBlog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        blog_id = request.POST.get("blog_id")
        desc = request.POST.get("desc")
        image = request.FILES.get("image")
        if title and desc:
            blog = Blogs.objects.get(id = blog_id)
            blog.title = title
            blog.decs = desc
            if image:
                blog.image = image
            blog.save()
            messages.success(request, 'Blog Updated')
            return HttpResponseRedirect(reverse('yourblog'))
        else:
            messages.error(request, 'Please Fill All the fileds')
            return HttpResponseRedirect(reverse('yourblog'))
    else:
        blogs = Blogs.objects.filter(author = request.user.id).order_by("-updated_at")
        return render(request,'yourblogs.html',{"blogs":blogs})


@login_required
def DeleteBlog(request,id):
    blog = Blogs.objects.filter(id = id,author = request.user.id)
    if blog.exists():
        blog.first().delete()
        messages.success(request, 'Blog Deleted')
        return HttpResponseRedirect(reverse('yourblog'))
    else:
        messages.error(request, 'Can not find any blog')
        return HttpResponseRedirect(reverse('yourblog'))