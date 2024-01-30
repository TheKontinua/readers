"""mentoris URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("mentapp/", include("mentapp.urls")),
    path("katex/", views.katex, name="katex"),
    path("login/", views.login, name="login"),
    path("signUp/", views.sign_up, name="sign_up"),
    path("profile/", views.profile, name="profile"),
    path("profile/<uuid:user_id>/", views.user_info, name="user_info"),
    path('profile/edit/<uuid:user_id>/', views.user_edit, name='user_edit'),
    path("main/", views.main, name="main"),
    path("main/<int:volume_id>/", views.main, name="main_vol_chap"),
    path("main/<int:volume_id>/<chapter_id>/", views.chapter, name="chapter"),
    path("edit_quiz/<int:quiz_id>", views.edit_quiz, name="edit_quiz"),
    path("<str:page>/header.html/", views.header, name="header"),
    path("<str:page>/footer.html/", views.footer, name="footer")
    path("download_pdf/<int:blob_key>/", views.download_pdf, name='download_pdf'),
    path("upload_pdf/<path:pdf_path>/", views.upload_pdf, name='upload_pdf'),
]
