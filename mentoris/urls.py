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
<<<<<<< HEAD
<<<<<<< HEAD
=======
    re_path(r".*/header.html/", views.header, name="header"),
    re_path(r".*/footer.html/", views.footer, name="footer"),
<<<<<<< HEAD
>>>>>>> c2e8da3 (header)
=======
    path("", views.default, name="default"),
>>>>>>> 1170c32 (Fixed the Default Routing)
    path("admin/", admin.site.urls),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    path("cars/", include("mentapp.urls")),
=======
    path('admin/', admin.site.urls),
    path("mentapp/", include("mentapp.urls")),
<<<<<<< HEAD
>>>>>>> b1d7166 (Fixed loading landing.html and volume.html)
    path("katex/", views.katex, name="katex"),
<<<<<<< HEAD
=======
=======
>>>>>>> aabf7f6 (edit/delete quiz buttons)
    path("latex/", views.latex, name="latex_question"),
<<<<<<< HEAD
=======
>>>>>>> b409248 (create new support + redirect to edit_support)
    path("login/", views.login, name="login"),
>>>>>>> cd40d18 (Renamed question creation page)
=======
=======
        path("fetch_attachments/question/<int:question_id>/", views.fetch_attachments_question, name="fetch_attachments_question"),
=======
    path("fetch_attachments/question/<int:question_id>/", views.fetch_attachments_question, name="fetch_attachments_question"),
>>>>>>> f4d4c28 (Fix Editing Primary Email)
    path("fetch_attachments/support/<int:support_id>/", views.fetch_attachments_support, name="fetch_attachment_support"),
    path("fetch_attachments_inputs/support/<int:support_id>/", views.fetch_attachments_inputs_support, name="fetch_attachments_inputs_support"),
    path("fetch_attachments_inputs/question/<int:question_id>/<str:part>/", views.fetch_attachments_inputs_question, name="fetch_attachments_inputs_question"),
    path("latex_window/question/<int:question_id>/<str:part>/<int:width>/", views.latex_window_question, name = "latex_window_question"),
    path("latex_window/support/<int:support_id>/<int:width>/", views.latex_window_support, name="latex_window_support"),
>>>>>>> a943d23 (LaTeX macro ready, times out when saving due to pdf generation)
    path("login/", views.customLogin, name="login"),
<<<<<<< HEAD
>>>>>>> 355e08d (Login persistence working + private pages + admin corrections + user model changes + backend authadded + changes to settings)
=======
    path("login/", views.customLogin, name="login"),
>>>>>>> a84a86d (Fixing Request Authentication)
=======
    path('logoutCustom/', views.customLogout, name='logoutCustom'),
>>>>>>> a9ea21b (Working Logout Button, picture for logout button might be nice)
    path("signUp/", views.sign_up, name="sign_up"),
    path("verify_email/", views.verify_email, name="verify_email"),
    path(
        "verify_email/<uidb64>/<token>/",
        views.verify_email_confirm,
        name="verify_email_confirm",
    ),
    path("profile/", views.profile, name="profile"),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
    path("login/", views.login, name="login"),
>>>>>>> 755d62a (Configured formatting rules,)
=======
>>>>>>> f3a6090 (profile page)
=======
    path('profile/<uuid:user_id>/', views.user_info, name='user_info'),

>>>>>>> 91d40a5 (Able to populate fields from db)
=======
    path("profile/<uuid:user_id>/", views.user_info, name="user_info"),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> e58ea8e (Linked login page to the backend)
=======
    path('profile/edit/<uuid:user_id>/', views.user_edit, name='user_edit'),
<<<<<<< HEAD
>>>>>>> e153f37 (Edit profile page)
=======
    path('profile/edit/<uuid:user_id>/', views.user_edit, name='user_edit'),
>>>>>>> 62301bf (Updates username but the logic is not good)
=======
=======
    path("profile/edit/<uuid:user_id>/", views.user_edit, name="user_edit"),
    path("reset/", views.reset, name="reset"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("reset_password/<uidb64>/<token>/", views.verify_reset, name="verify_reset"),
    path("user_directory/", views.user_directory, name="user_directory"),
    path("promotion/", views.promotion, name="promotion"),
>>>>>>> 52968c0 (Implemented User Directory and Promotion Page)
    path("main/", views.main, name="main"),
    path("main/<int:volume_id>/", views.main, name="main_vol_chap"),
<<<<<<< HEAD

>>>>>>> 7fc2710 (main page volume + chapter selector)
=======
    path("main/<int:volume_id>/<chapter_id>/", views.chapter, name="chapter"),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 17adf3a (Implemented the Chapter Page with Quiz Information)
=======
=======
    path("main/<int:volume_id>/<chapter_id>/<int:quiz_id>", views.quiz, name="quiz"),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    path("main/<int:volume_id>/<chapter_id>/<int:quiz_id>/maker_view", views.quiz_maker_view, name="quiz_maker_view"),
>>>>>>> 0ae4eb6 (Merging Base Feedback w/ Main)
    path("edit_quiz/<int:quiz_id>", views.edit_quiz, name="edit_quiz"),
<<<<<<< HEAD
    path("edit_quiz_add_question/<int:quiz_id>", views.edit_quiz_add_question, name="edit_quiz_add_question"),
    path("edit_quiz_add_support/<int:quiz_id>", views.edit_quiz_add_support, name="edit_quiz_add_support"),
<<<<<<< HEAD
<<<<<<< HEAD
    path("<str:page>/header.html/", views.header, name="header"),
<<<<<<< HEAD
    path("<str:page>/footer.html/", views.footer, name="footer")
>>>>>>> f354f38 (edit quiz page, added header and footer html files, and colors css file)
=======
    path('download_pdf/<int:blob_key>/', views.download_pdf, name='download_pdf'),
<<<<<<< HEAD
>>>>>>> 906fe04 (download works)
=======
    path('upload_pdf/<path:pdf_path>/', views.upload_pdf, name='upload_pdf'),
>>>>>>> 5eb3753 (upload pdfs)
=======
=======
    path("<str:page>/footer.html/", views.footer, name="footer"),
>>>>>>> c02fa63 (Fixed minor syntax error)
=======
    re_path(r".*/header.html/", views.header, name="header"),
    re_path(r".*/footer.html/", views.footer, name="footer"),
>>>>>>> c745f59 (Update urls.py)
=======
>>>>>>> c2e8da3 (header)
    path("download_pdf/<int:blob_key>/", views.download_pdf, name='download_pdf'),
<<<<<<< HEAD
    path("upload_pdf/<path:pdf_path>/", views.upload_pdf, name='upload_pdf'),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 98cd03b (pr changes)
=======
    path('quiz/create/', views.create_quiz, name='create_quiz'),
>>>>>>> a206368 (Fixed styling and added more elements)
=======
=======
    path("create_support/", views.create_support, name="create_support"),

>>>>>>> 0e18c57 (add attachments and blobs to db)
    path('quiz/create/<int:volume_id>/<chapter_id>', views.create_quiz, name='create_quiz'),
>>>>>>> 43a9a53 (Updated changes so that make quiz instantiates the volume and chapter)
=======
    path("create_support/", views.create_support, name="create_support"),
>>>>>>> 324f15d (support view and url)
]
=======
=======
    path("create_support/", views.create_support, name="create_support"),
    path('quiz/create/<int:volume_id>/<chapter_id>', views.create_quiz, name='create_quiz'),
    path('delete_quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),

>>>>>>> aabf7f6 (edit/delete quiz buttons)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 6684e51 (Display question attachments implemented, needed to add MEDIA_URL and MEDIA_ROOT in settings.py and modify urls.py to serve user created images.)
=======
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
    re_path(r".*/header.html/", views.header, name="header"),
    re_path(r".*/footer.html/", views.footer, name="footer"),
    path("download_pdf/<int:quiz_id_str>/", views.download_pdf, name="download_pdf"),
    path("upload_pdf/<path:pdf_path>/", views.upload_pdf, name="upload_pdf"),
    path("create_support/", views.create_support, name="create_support"),
=======
=======
>>>>>>> 1170c32 (Fixed the Default Routing)
    path(
        "main/<int:volume_id>/<chapter_id>/<int:quiz_id>/maker_view",
        views.quiz_maker_view,
        name="quiz_maker_view",
    ),
<<<<<<< HEAD
=======
    path("main/<int:volume_id>/<chapter_id>/<int:quiz_id>/maker_view", views.quiz_maker_view, name="quiz_maker_view"),
>>>>>>> b96e408 (urls.py formatting)
=======
>>>>>>> 1170c32 (Fixed the Default Routing)
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
<<<<<<< HEAD
    path("create_support/", views.create_support, name="create_support"),
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 2889b3c (Download PDF bug fix)
=======
>>>>>>> 1170c32 (Fixed the Default Routing)
    path(
        "quiz/create/<int:volume_id>/<chapter_id>",
        views.create_quiz,
        name="create_quiz",
    ),
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
    path("edit_support/<int:support_id>/", views.edit_support, name="edit_support"),
>>>>>>> b409248 (create new support + redirect to edit_support)
=======
    path("create_support/<int:quiz_id>", views.create_support, name="create_support"),
<<<<<<< HEAD
    path("edit_support/<int:quiz_id>/<int:support_id>/", views.edit_support, name="edit_support"),
>>>>>>> ac19015 (edit supports)
    path("quiz/create/<int:volume_id>/<chapter_id>", views.create_quiz, name="create_quiz"),
=======
>>>>>>> 1170c32 (Fixed the Default Routing)
=======
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
>>>>>>> a84a86d (Fixing Request Authentication)
    path("delete_quiz/<int:quiz_id>/", views.delete_quiz, name="delete_quiz"),
    path("create_question/", views.create_question, name="create_question"),
    path("edit_question/<int:question_id>/", views.edit_question, name="edit_question"),
>>>>>>> 472b9a9 (edit buttons redirect)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 7e40b51 (Download functionality to chapter page)
=======
=======
    path("quiz/create/<int:volume_id>/<chapter_id>", views.create_quiz, name="create_quiz"),
>>>>>>> b96e408 (urls.py formatting)
    path("delete_quiz/<int:quiz_id>/", views.delete_quiz, name="delete_quiz"),
    path("question_approval/", views.question_approval, name="question_approval"),
    path("handles/", views.handles, name="handles"),
    path('delete-handle/<str:handle>/<int:site_id>/<uuid:user_id>', views.delete_handle, name='delete_handle'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 2889b3c (Download PDF bug fix)
