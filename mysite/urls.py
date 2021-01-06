"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from donors.views import signup_user, dashboard, logout_user, login_user, profile, mail_user, messages, home

urlpatterns = [
    path('admin/', admin.site.urls),

    #authentication
    path('signup/', signup_user, name='signup_user'),
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    #navigation
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('mail/<int:donor_pk>', mail_user, name='mail'),
    path('messages/', messages, name='messages'),
    path('', home, name='home')
]
