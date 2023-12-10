from django.http import HttpResponse
from django.template import loader
from mentapp.models import User, Email, Volume, Chapter, Chapter_Loc
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from mentoris.forms import UserForm
from django.core.mail import send_mail


def katex(request):
    template = loader.get_template("katex/index.html")
    return HttpResponse(template.render())


def sign_up(request):
    if request.method == "POST":
        # Add to User table
        form = UserForm(request.POST)

        if form.is_valid():
            email_exists = False
            other_email_exists = False

            if Email.objects.filter(
                email_address=request.POST.get("email_address")
            ).exists():
                email_exists = True

            other_emails = request.POST.get("other_emails")
            if other_emails is not None and other_emails != "":
                email_list = other_emails.split(",")
                for other_email in email_list:
                    if Email.objects.filter(email_address=other_email.strip()).exists():
                        other_email_exists = True

            # TODO: Change location of error message to be in proper place based on exists
            if email_exists or other_email_exists:
                if email_exists:
                    form.add_error(None, "Primary")
                if other_email_exists:
                    form.add_error(None, "Other")
                return render(
                    request,
                    "mentapp/sign_up.html",
                    {
                        "form": form,
                        "email": request.POST.get("email_address"),
                        "other_emails": request.POST.get("other_emails"),
                    },
                )
            user = form.save()
            # Add to Email table
            email = request.POST.get("email_address")
            emailObject = Email()
            emailObject.email_address = email
            emailObject.user = user
            emailObject.is_primary = True
            emailObject.save()

            other_emails = request.POST.get("other_emails")
            if other_emails is not None and other_emails != "":
                email_list = other_emails.split(",")
                for other_email in email_list:
                    emailObject = Email()
                    emailObject.email_address = other_email.strip()
                    emailObject.user = user
                    emailObject.is_primary = False
                    emailObject.save()

            return redirect(f"../profile/{user.user_id}")

        return render(
            request,
            "mentapp/sign_up.html",
            {
                "form": form,
            },
        )
    else:
        return render(request, "mentapp/sign_up.html")


def profile(request):
    template = loader.get_template("mentapp/profile.html")
    return HttpResponse(template.render())


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password_hash")

        try:
            emailObject = Email.objects.get(email_address=email)
            user = emailObject.user
            if not user.check_password(password):
                user = None
        except Email.DoesNotExist:
            user = None

        if user is not None:
            # TODO: log user in
            return redirect(f"../profile/{user.user_id}")
        else:
            messages.error(
                request,
                "Could not find account, please double-check account credentials",
            )
            return render(
                request,
                "mentapp/login.html",
                {"email": email, "password": password},
            )
    else:
        return render(request, "mentapp/login.html")


def user_info(request, user_id):
    user_profile = get_object_or_404(User, user_id=user_id)
    try:
        email = Email.objects.get(user_id=user_id, is_primary=True)
        other_emails = Email.objects.filter(user_id=user_id, is_primary=False)
        other_emailss = [obj.email_address for obj in other_emails]
        other_email = ", ".join(other_emailss)
    except Email.DoesNotExist:
        email = None
    return render(
        request,
        "mentapp/profile.html",
        {"user_profile": user_profile, "email": email, "other_email": other_email},
    )


def user_edit(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    # print("user items", user)
    # print("request items", request.POST)
    for key, value in request.POST.items():
        # print("KEY", key, "VALUE", value)
        if key == "primary_email":
            Email.objects.filter(user_id=user_id, is_primary=True).update(
                email_address=value
            )
        if key == "other_emails":
            Email.objects.filter(user_id=user_id, is_primary=False).delete()
            insEmails = value.split(",")
            for em in insEmails:
                emailObject = Email()
                emailObject.email_address = em
                emailObject.user_id = user_id
                emailObject.save()
        # Check if the user object has this field and the value is not empty
        if hasattr(user, key) and value.strip():
            # print("USERKEY", key, "USERVAL", value)
            setattr(user, key, value)
    user.save()
    return redirect(f"/profile/{user.user_id}")


def request_translation(request, user_id):
    # need to verify email to ses when they sign up in order for this to work
    email = get_object_or_404(Email, user_id=user_id, is_primary=True)
    primary_language = get_object_or_404(User.primary_language, user_id=user_id)
    send_mail(
        "Kontinua Quiz Questions Translations Request",
        "Hi there! We have noticed you are fluent in "
        + primary_language
        + ". This week these questions were added in "
        + primary_language
        + ". I can do a preliminary translation to "
        + primary_language
        + " using Google Translate. Would you look at and correct those preliminary translations?  Click here.",
        "notifications@kontinua.org",
        [email],
    )

def main(request, volume_id = 1):
    template = loader.get_template("mentapp/main.html")

    volumes = Volume.objects.values_list('volume_id', flat=True).distinct().order_by('volume_id')

    if volume_id:
        chapters = Chapter.objects.filter(volume__volume_id=volume_id).distinct()    
    else:
        chapters = []

    chapter_locs = Chapter_Loc.objects.filter(chapter__chapter_id__in=chapters).distinct()
   
    context = {'volumes': volumes, "chapters": chapters, "volume_id": volume_id, "chapter_locs": chapter_locs}

    return HttpResponse(template.render(context, request))






