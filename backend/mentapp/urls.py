from django.urls import path

from . import views

from django.urls import path





urlpatterns = [

    path("<int:volume_number>/", views.volume_chapter, name="volume_chapter"),
    path("", views.volumes, name="volumes")
] 

