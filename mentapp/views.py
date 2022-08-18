from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from mentapp.models import Chapter_Loc, Volume, Chapter




def volume(request, volume_number):

    volume = Volume.objects.get(number=volume_number)
    chapters = Chapter.objects.filter(volume=volume)
    chapters_loc = Chapter_Loc.objects.filter(chapter__in=chapters).order_by('chapter.chapter_ordering')
    
    return render(request, 'mentapp/volume.html', {'volume': volume, 'chapters': chapters_loc}) 
