"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.Login,name='login'),
    path('signup',views.Signup,name='signup'),
    path('logout',views.Logout,name='logout'),
    path('blogs',views.Allblog,name='blogs'),
    path('blog/<str:id>',views.Blog,name='blog'),
    path('add/blog/',views.AddBlog,name='addblog'),
    path('your/blog/',views.YourBlog,name='yourblog'),
    path('blog/delete//<str:id>',views.DeleteBlog,name='deleteblog'),


    
]
