from datetime import datetime
from email.mime import application
from multiprocessing import context
from xml.etree.ElementTree import Comment
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect,render
from itsdangerous import json
from myblog.models import Blogs,Comments
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

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
    is_like =  request.user in blog.like.all()
    is_dislike = request.user in blog.dislike.all()
    comments = Comments.objects.filter(blog=id).exclude(user=request.user.id).select_related('user','blog').order_by('-created_at')
    user_comments = Comments.objects.filter(blog=id,user=request.user.id).select_related('user','blog').order_by('-created_at')
    context={"blogs":blogs,"blog":blog,"is_like":is_like,"is_dislike":is_dislike,
    "total_comments":Comments.objects.filter(blog = blog.id).count(),"user_comments":user_comments,"comments":comments}
    print(context)
    return render(request,'blog.html',context)

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


@login_required
@csrf_exempt
def AddLike(request):
    try:
        if not request.method == "POST":
            data={"success":False,"message":"Method must be Post"}
            return JsonResponse(data,safe=False)
        blog_id =  request.POST.get('blog_id')
        blog = Blogs.objects.filter(id = blog_id)
        if blog.exists():
            if not blog.filter(like =  request.user.id).exists():
                blog = blog.first()
                blog.dislike.remove(request.user)
                blog.like.add(request.user)
                data={"success":True,"message":"Added","total_like":blog.total_like(),"total_dislike":blog.total_dislike()}
                return JsonResponse(data,safe=False)
            else:
                blog = blog.first()
                blog.dislike.remove(request.user)
                blog.like.remove(request.user)
                data={"success":True,"message":"Removed","total_like":blog.total_like(),"total_dislike":blog.total_dislike()}
                return JsonResponse(data,safe=False)
        else:
            data={"success":False,"message":"Blog not Exist"}
            return JsonResponse(data,safe=False)
    except Exception as e:
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        data={"success":False,"message":str(e)}
        return JsonResponse(data,safe=False)


@login_required
@csrf_exempt
def AddDisLike(request):
    try:
        if not request.method == "POST":
            data={"success":False,"message":"Method must be Post"}
            return JsonResponse(data,safe=False)
        blog_id =  request.POST.get('blog_id')
        blog = Blogs.objects.filter(id = blog_id)
        if blog.exists():
            if not blog.filter(dislike = request.user.id).exists():
                blog = blog.first()
                blog.like.remove(request.user)
                blog.dislike.add(request.user)
                data={"success":True,"message":"Added","total_like":blog.total_like(),"total_dislike":blog.total_dislike()}
                return JsonResponse(data,safe=False)
            else:
                blog = blog.first()
                blog.like.remove(request.user)
                blog.dislike.remove(request.user)
                data={"success":True,"message":"Removed","total_like":blog.total_like(),"total_dislike":blog.total_dislike()}
                return JsonResponse(data,safe=False)
        else:
            data={"success":False,"message":"Blog not Exist"}
            return JsonResponse(data,safe=False)
    except Exception as e:
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        data={"success":False,"message":str(e)}
        return JsonResponse(data,safe=False)


@login_required
@csrf_exempt
def AddComment(request):
    try:
        if not request.method == "POST":
            data={"success":False,"message":"Method must be Post"}
            return JsonResponse(data,safe=False)
        blog_id =  request.POST.get('blog_id')
        text =  request.POST.get('text')
        blog = Blogs.objects.filter(id = blog_id)
        if blog.exists():
            blog = blog.first()
            comment = Comments(text=text,blog=blog,user=request.user)
            comment.save()
            data={"success":True,"message":"Added","total_comments":Comments.objects.filter(blog = blog.id).count(),"publish":comment.created_at.strftime('%b %d, %Y, %I:%M %p')}
            return JsonResponse(data,safe=False)
        else:
            data={"success":False,"message":"Blog not Exist"}
            return JsonResponse(data,safe=False)
    except Exception as e:
        print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
        data={"success":False,"message":str(e)}
        return JsonResponse(data,safe=False)
