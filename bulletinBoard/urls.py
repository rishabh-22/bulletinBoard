"""bulletinBoard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from user_auth import views as auth_view
from board import views as board_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', auth_view.Register.as_view()),
    path('login/', auth_view.Login.as_view()),
    path('board/', board_view.BoardList.as_view()),
    path('board/<str:pk>', board_view.BoardDetail.as_view()),
    path('moderator/', board_view.ModeratorList.as_view()),
    path('thread/', board_view.ThreadDetail.as_view()),
    path('post/', board_view.PostList.as_view()),
]
