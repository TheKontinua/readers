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
from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.conf import settings


urlpatterns = [
    re_path(r".*/header.html/", views.header, name="header"),
    re_path(r".*/footer.html/", views.footer, name="footer"),
    path("", views.default, name="default"),
    path("admin/", admin.site.urls),
        path("fetch_attachments/question/<int:question_id>/", views.fetch_attachments_question, name="fetch_attachments_question"),
    path("fetch_attachments/support/<int:support_id>/", views.fetch_attachments_support, name="fetch_attachment_support"),
    path("fetch_attachments_inputs/support/<int:support_id>/", views.fetch_attachments_inputs_support, name="fetch_attachments_inputs_support"),
    path("fetch_attachments_inputs/question/<int:question_id>/<str:part>/", views.fetch_attachments_inputs_question, name="fetch_attachments_inputs_question"),
    path("latex_window/question/<int:question_id>/<str:part>/<int:width>/", views.latex_window_question, name = "latex_window_question"),
    path("latex_window/support/<int:support_id>/<int:width>/", views.latex_window_support, name="latex_window_support"),
    path("login/", views.customLogin, name="login"),
    path('logoutCustom/', views.customLogout, name='logoutCustom'),
    path("signUp/", views.sign_up, name="sign_up"),
    path("verify_email/", views.verify_email, name="verify_email"),
    path(
        "verify_email/<uidb64>/<token>/",
        views.verify_email_confirm,
        name="verify_email_confirm",
    ),
    path("profile/", views.profile, name="profile"),
    path("profile/<uuid:user_id>/", views.user_info, name="user_info"),
    path("profile/edit/<uuid:user_id>/", views.user_edit, name="user_edit"),
    path("reset/", views.reset, name="reset"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("reset_password/<uidb64>/<token>/", views.verify_reset, name="verify_reset"),
    path("user_directory/", views.user_directory, name="user_directory"),
    path("promotion/", views.promotion, name="promotion"),
    path("main/", views.main, name="main"),
    path("main/<int:volume_id>/", views.main, name="main_vol_chap"),
    path("main/<int:volume_id>/<chapter_id>/", views.chapter, name="chapter"),
    path("main/<int:volume_id>/<chapter_id>/<int:quiz_id>", views.quiz, name="quiz"),
    path(
        "main/<int:volume_id>/<chapter_id>/<int:quiz_id>/maker_view",
        views.quiz_maker_view,
        name="quiz_maker_view",
    ),
    path("edit_quiz/<int:quiz_id>", views.edit_quiz, name="edit_quiz"),
    path(
        "edit_quiz_add_question/<int:quiz_id>",
        views.edit_quiz_add_question,
        name="edit_quiz_add_question",
    ),
    path(
        "edit_quiz_add_support/<int:quiz_id>",
        views.edit_quiz_add_support,
        name="edit_quiz_add_support",
    ),
    path("download_pdf/<int:quiz_id>/", views.download_pdf, name="download_pdf"),
    path("create_support/<int:quiz_id>", views.create_support, name="create_support"),
    path(
        "edit_support/<int:quiz_id>/<int:support_id>/",
        views.edit_support,
        name="edit_support",
    ),
    path(
        "quiz/create/<int:volume_id>/<chapter_id>",
        views.create_quiz,
        name="create_quiz",
    ),
    path("delete_quiz/<int:quiz_id>/", views.delete_quiz, name="delete_quiz"),
    path("create_question/", views.create_question, name="create_question"),
    path("edit_question/<int:question_id>/", views.edit_question, name="edit_question"),
    path("question_approval/", views.question_approval, name="question_approval"),
    path("handles/", views.handles, name="handles"),
    path('delete-handle/<str:handle>/<int:site_id>/<uuid:user_id>', views.delete_handle, name='delete_handle'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
