from django.http import HttpResponse
from django.template import loader
from mentapp.models import User, Email
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from mentoris.forms import UserForm


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
            email = request.POST.get("primary_email")
            emailObject = Email()
            emailObject.primary_email = email
            emailObject.user_id = user
            emailObject.is_primary = True
            emailObject.save()

            other_emails = request.POST.get("other_emails")
            # TODO: This assumes that the input field is properly inputted
            if other_emails is not None:
                email_list = other_emails.split(", ")
                for other_email in email_list:
                    emailObject = Email()
                    emailObject.primary_email = other_email
                    emailObject.user_id = user
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
    email = get_object_or_404(Email, user_id=user_id, is_primary=True)
    return render(
        request, "mentapp/profile.html", {"user_profile": user_profile, "email": email}
    )
