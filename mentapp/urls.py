from django.urls import path

from . import views



urlpatterns = [

    path("<int:volume_number>/", views.volume_chapter, name="volume_chapter"),
    path("", views.volumes, name="volumes"),
]
