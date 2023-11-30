from django.http import HttpResponse
from django.template import loader
from mentapp.models import User, Email
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
                    emailObject.email_address = other_email
                    emailObject.user = user
                    emailObject.save()

            return redirect(f"../profile/{user.user_id}")

        return render(request, "mentapp/sign_up.html", {"form": form})
    else:
        return render(request, "mentapp/sign_up.html")


def profile(request):
    template = loader.get_template("mentapp/profile.html")
    return HttpResponse(template.render())


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(display_name=username, password=password)
        except User.DoesNotExist:
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
                {"username": username, "password": password},
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
                emailObject.user_id = user
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
