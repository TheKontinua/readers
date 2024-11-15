from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from mentapp.models import Chapter_Loc, Volume, Chapter

def volume_chapter(request, volume_number):

    volume = Volume.objects.get(number=volume_number)
    chapters = Chapter.objects.filter(volume=volume)
    chapters_loc = Chapter_Loc.objects.filter(chapter__in=chapters).order_by('chapter')
    
    return render(request, 'mentapp/volume.html', {'volume': volume, 'chapters': chapters_loc}) 

def volumes(request):
    volumes = Volume.objects.filter()
    return render(request, 'mentapp/landing.html', {'volumes': volumes})