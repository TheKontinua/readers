from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from mentapp.models import Chapter_Loc, Volume, Chapter
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import AppFeedback


def volume_chapter(request, volume_number):

    volume = Volume.objects.get(number=volume_number)
    chapters = Chapter.objects.filter(volume=volume)
    chapters_loc = Chapter_Loc.objects.filter(chapter__in=chapters).order_by("chapter")

    return render(
        request, "mentapp/volume.html", {"volume": volume, "chapters": chapters_loc}
    )


def volumes(request):
    volumes = Volume.objects.filter()
    return render(request, "mentapp/landing.html", {"volumes": volumes})


@csrf_exempt  # Only for testing
def submit_feedback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            feedback_text = data.get("feedback")

            if not email or not feedback_text:
                return JsonResponse(
                    {"status": "error", "message": "Email and feedback are required"},
                    status=400,
                )

            feedback = AppFeedback.objects.create(
                email=email, feedback_text=feedback_text
            )

            return JsonResponse(
                {"status": "success", "message": "Feedback submitted successfully"}
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "message": "Only POST method is allowed"}, status=405
    )
