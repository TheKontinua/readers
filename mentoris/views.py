import base64
import json, os, random
from datetime import date
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from mentapp.models import User, Email, Volume, Chapter, Chapter_Loc, Question_Loc, Quiz, Quiz_Question, Question
=======
from mentapp.models import User, Email, Volume, Chapter, Chapter_Loc, Blob
>>>>>>> 906fe04 (download works)
=======
=======
from django.core.files.storage import FileSystemStorage
>>>>>>> 0e18c57 (add attachments and blobs to db)
=======
from django.core.files.storage import FileSystemStorage
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> e813f48 (add attachments and blobs to db)
=======
=======
>>>>>>> de7f334 (Creator fields, no questions edge case, deleted imports)
from django.urls import resolve
>>>>>>> aabf7f6 (edit/delete quiz buttons)
=======
from django.core.exceptions import ValidationError
from django.urls import resolve, reverse
>>>>>>> 8faf4bf (Handles page done)
=======
from django.template.loader import render_to_string
from django.urls import resolve
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from functools import wraps
>>>>>>> e5984d8 (Implement Email Verification & Password Reset)
from mentapp.models import (
    Handle,
    Question_Attachment,
    Quiz_Rendering,
    Site,
    User,
    Email,
    Volume,
    Chapter,
    Chapter_Loc,
    Blob,
    Question_Loc,
    Quiz,
    Quiz_Question,
    Quiz_Rendering,
    Quiz_Feedback,
    Question,
    Verification,
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 324f15d (support view and url)
    Question_Attachment,
    Support,
    Support_Loc,
<<<<<<< HEAD
    Support_Attachment
<<<<<<< HEAD
=======
    Question_Attachment
>>>>>>> e813f48 (add attachments and blobs to db)
=======
>>>>>>> 324f15d (support view and url)
=======
    Support_Attachment,
<<<<<<< HEAD
<<<<<<< HEAD
    Quiz_Support
>>>>>>> 0f14dbf (view supports)
=======
    Quiz_Support,
>>>>>>> c58b4ad (Initial changes for pdf rendering)
=======
    Site,
    Quiz_Support,
<<<<<<< HEAD
    Handle
>>>>>>> f94ffd3 (Issues with model definitions)
=======
    Handle,
>>>>>>> f4d4c28 (Fix Editing Primary Email)
)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 981eeea (Submit questions to database)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
<<<<<<< HEAD
<<<<<<< HEAD
from mentoris.forms import UserForm
<<<<<<< HEAD
=======
=======
from mentoris.forms import QuizForm
import json, random
>>>>>>> f354f38 (edit quiz page, added header and footer html files, and colors css file)
=======
from mentoris.forms import UserForm, LatexForm
>>>>>>> 54c7560 (Changed katex page to use LaTeX.js)
from django.core.mail import send_mail
<<<<<<< HEAD
from django.http import JsonResponse
=======
=======
from mentoris.forms import UserForm, LatexForm, QuizForm
=======
from mentoris.forms import UserForm, LatexForm
>>>>>>> de7f334 (Creator fields, no questions edge case, deleted imports)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
>>>>>>> 52968c0 (Implemented User Directory and Promotion Page)
from django.core.files.base import ContentFile
<<<<<<< HEAD
from datetime import date
<<<<<<< HEAD

<<<<<<< HEAD
=======
from django.contrib.auth.decorators import login_required
>>>>>>> 355e08d (Login persistence working + private pages + admin corrections + user model changes + backend authadded + changes to settings)
from mentoris.latex_to_pdf import latex_to_pdf
<<<<<<< HEAD
=======

>>>>>>> f775257 (Initial changes for pdf rendering)

<<<<<<< HEAD
<<<<<<< HEAD

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 5eb3753 (upload pdfs)

>>>>>>> 0b5462f (Implemented Request Translation Email Notification)

def katex(request):
    template = loader.get_template('katex/index.html')
    return HttpResponse(template.render())

<<<<<<< HEAD
<<<<<<< HEAD
=======

<<<<<<< HEAD
def login(request):
    template = loader.get_template("mentapp/login.html")
    return HttpResponse(template.render())
=======

=======
>>>>>>> 981eeea (Submit questions to database)
=======
=======

>>>>>>> dfddf8a (Getting current user to populate empty fields)
@login_required
>>>>>>> 1c66536 (Restrict add question to quizmaker and above)
=======
from mentoris.latex_to_pdf import latex_to_pdf
from functools import wraps

=======
from mentoris.email_verification_token_generator import email_verification_token
from mentoris.forms import UserForm, LatexForm, QuizForm
from mentoris.latex_to_pdf import latex_to_pdf

>>>>>>> e5984d8 (Implement Email Verification & Password Reset)

def mentor_req(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Checking that there is a logged in user else return to the login page
        if not request.user.is_authenticated:
            return render(request, "mentapp/login.html")
        # Checking that user is mentor (verified) or higher else returning an error
        if not (
            request.user.is_quizmaker
            or request.user.is_admin
            or request.user.is_verified
        ):
            return HttpResponseForbidden(
                "Forbidden: Must be mentor or quizmaker to access add questions page. Use request verification for mentor status"
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def quizmaker_req(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Checking that there is a logged in user else return to the login page
        if not request.user.is_authenticated:
            return render(request, "mentapp/login.html")
        # Checking user is quiz maker or higher else returning forbidden HTTP page.
        if not (request.user.is_quizmaker or request.user.is_admin):
            return HttpResponseForbidden(
                "Forbidden: Must be quizmaker or admin to access edit quiz. Must request verification"
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def admin_req(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Checking that there is a logged in user else return to the login page
        if not request.user.is_authenticated:
            return redirect("admin:login")
        # Must be admin!
        if not request.user.is_admin:
            return HttpResponseForbidden("Forbidden: Must be admin to access.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@mentor_req
<<<<<<< HEAD
>>>>>>> ccfcdc2 (Decorators n pages)
def latex(request):
<<<<<<< HEAD
=======
    if (
        request.user.is_quizmaker == False
        and request.user.is_admin == False
        and request.user.is_verified == False
    ):
        return HttpResponseForbidden(
            "Forbidden: Must be mentor or quizmaker to access add questions page."
        )
>>>>>>> dfddf8a (Getting current user to populate empty fields)
=======
def latex(request, question_id):
>>>>>>> a943d23 (LaTeX macro ready, times out when saving due to pdf generation)
    volumes = (
        Volume.objects.values_list("volume_id", flat=True)
        .distinct()
        .order_by("volume_id")
    )

    volume_id = 1
    chapters = Chapter.objects.filter(volume__volume_id=volume_id).distinct()

    chapter_locs = Chapter_Loc.objects.filter(
        chapter__chapter_id__in=chapters
    ).distinct()

    chapter_object = chapter_locs[0]

    if request.method == "POST":
        if request.POST.get("command") == "deleteAttachment":
            question = get_object_or_404(Question, question_id=question_id)
            question_loc = get_object_or_404(
                Question_Loc, question=question, lang_code="ENG", dialect_code="US"
            )
            attachment = get_object_or_404(
                Question_Attachment,
                question=question_loc,
                filename=request.POST.get("filename"),
            )
            attachment.blob_key.delete()
            attachment.delete()
            return JsonResponse({"success": True})

        if request.POST.get("command") == "answer":
            question = get_object_or_404(Question, question_id=question_id)
            question_loc = get_object_or_404(
                Question_Loc, question=question, lang_code="ENG", dialect_code="US"
            )
            question_loc.answer_latex = request.POST.get("input")
            question_loc.save()
            return JsonResponse({"success": True})

        if request.POST.get("command") == "rubric":
            question = get_object_or_404(Question, question_id=question_id)
            question_loc = get_object_or_404(
                Question_Loc, question=question, lang_code="ENG", dialect_code="US"
            )
            question_loc.rubric_latex = request.POST.get("input")
            question_loc.save()
            return JsonResponse({"success": True})

        if request.POST.get("command") == "question":
            question = get_object_or_404(Question, question_id=question_id)
            question_loc = get_object_or_404(
                Question_Loc, question=question, lang_code="ENG", dialect_code="US"
            )
            question_loc.question_latex = request.POST.get("input")
            question_loc.save()
            return JsonResponse({"success": True})

        if request.POST.get("command") == "upload":
            question = get_object_or_404(Question, question_id=question_id)
            question_loc = get_object_or_404(
                Question_Loc, question=question, lang_code="ENG", dialect_code="US"
            )
            for filename, file in request.FILES.items():
                name = filename[0 : filename.rfind(".")]
                blob = Blob(file=file, content_type=file.content_type, filename=name)
                attachment = Question_Attachment(
                    question=question_loc, blob_key=blob, filename=name
                )
                blob.save()
                attachment.save()

            return JsonResponse({"success": True, "url": blob.file.url, "name": name})
        form = LatexForm(request.POST)
        question = request.POST.get("latex_question")
        answer = request.POST.get("latex_answer")
        grading = request.POST.get("latex_grading")
        volume_id = request.POST.get("volume")
        volume_id = int(volume_id)
        chapters = Chapter.objects.filter(volume__volume_id=volume_id).distinct()

        chapter_locs = Chapter_Loc.objects.filter(
            chapter__chapter_id__in=chapters
        ).distinct()

        if "submit-question" in request.POST:
            question_object = Question()
            question_loc = Question_Loc()

            # TODO: question_object.creator = CURRENT USER

            chapter_object = request.POST.get("chapter")
            chapter_string = chapter_object.split("_")
            chapter_title = chapter_string[0]
            chapter_loc = get_object_or_404(Chapter_Loc, title=chapter_title)
            question_object.chapter = chapter_loc.chapter

            question_object.conceptual_difficulty = request.POST.get("difficulty")
            question_object.time_required_mins = request.POST.get("time_required")
            question_object.point_value = request.POST.get("points")
            question_object.pages_required = request.POST.get("pages_required")
            question_object.save()

            question_loc.question = question_object
            question_loc.question_latex = question
            question_loc.answer_latex = answer
            question_loc.rubric_latex = grading

            question_loc.save()

<<<<<<< HEAD
            question_attachments = request.FILES.getlist("attachments")

            for attachment in question_attachments:

                blob = Blob(
                    file=attachment,
                    content_type=attachment.content_type,
                    filename=attachment.name,
                )
                blob.save()

                question_attachment_instance = Question_Attachment(
                    question=question_loc,
<<<<<<< HEAD
                    lang_code = question_loc.lang_code,
                    dialect_code = question_loc.dialect_code,
<<<<<<< HEAD
<<<<<<< HEAD
                    filename=blob.filename,
=======
                    filename=blob.file,
>>>>>>> e813f48 (add attachments and blobs to db)
=======
                    filename=blob.filename,
>>>>>>> 324f15d (support view and url)
                    blob_key = blob
=======
                    lang_code=question_loc.lang_code,
                    dialect_code=question_loc.dialect_code,
                    filename=blob.filename,
                    blob_key=blob,
>>>>>>> c58b4ad (Initial changes for pdf rendering)
                )
                question_attachment_instance.save()

=======
>>>>>>> f775257 (Initial changes for pdf rendering)
            chapter_id = chapter_loc.chapter.chapter_id

            return redirect(f"../main/{volume_id}/{chapter_id}")

        if "volume-button" not in request.POST:
            chapter_object = request.POST.get("chapter")
            chapter_string = chapter_object.split("_")
            chapter_title = chapter_string[0]
            chapter_object = get_object_or_404(Chapter_Loc, title=chapter_title)
        else:
            chapter_object = chapters[0]

        return render(
            request,
            "mentapp/latex_question.html",
            {
                "question_id": question_id,
                "form": form,
                "question": question,
                "answer": answer,
                "grading": grading,
                "volume_id": volume_id,
                "volumes": volumes,
                "chapters": chapter_locs,
                "chapter": chapter_object,
            },
        )
    else:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        return render(request, "katex/index.html", {"form": LatexForm()})
>>>>>>> 54c7560 (Changed katex page to use LaTeX.js)
=======
        return render(request, "mentapp/latex_question.html", {"form": LatexForm()})
>>>>>>> cd40d18 (Renamed question creation page)
=======
        print(chapters)
=======
>>>>>>> c663886 (remove prints)
=======
>>>>>>> f775257 (Initial changes for pdf rendering)
        return render(
            request,
            "mentapp/latex_question.html",
            {
                "form": LatexForm(),
                "volumes": volumes,
                "volume_id": volume_id,
                "chapters": chapter_locs,
                "chapter": chapter_object,
<<<<<<< HEAD
=======
            },
        )


<<<<<<< HEAD
def test_latex(request):
    if request.method == "POST":
        form = LatexForm(request.POST)
        question = request.POST.get("latex_question")
        return render(
            request,
            "mentapp/latex_test.html",
            {
                "form": form,
                "question": question,
            },
        )
    else:
        return render(
            request,
            "mentapp/latex_test.html",
            {
                "form": LatexForm(),
>>>>>>> f775257 (Initial changes for pdf rendering)
            },
        )
>>>>>>> 981eeea (Submit questions to database)


>>>>>>> 6502796 (Merged in changes from sign up page)
=======
>>>>>>> e58ea8e (Linked login page to the backend)
=======
>>>>>>> b409248 (create new support + redirect to edit_support)
=======
def default(request):
    if not request.user or hasattr(request, "user"):
        return redirect(f"../login")
    elif not request.user.is_verified:
        return redirect(f"../profile/{request.user.user_id}")
    else:
        return redirect(f"../main")


>>>>>>> 1170c32 (Fixed the Default Routing)
def sign_up(request):
<<<<<<< HEAD
    template = loader.get_template('mentapp/sign_up.html')
    return HttpResponse(template.render())
=======
    if request.method == "POST":
        # Add to User table
        form = UserForm(request.POST)
<<<<<<< HEAD

<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 355e08d (Login persistence working + private pages + admin corrections + user model changes + backend authadded + changes to settings)
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
<<<<<<< HEAD
            user = form.save()
>>>>>>> d0e2fad (Added basic email validation to sign_up page)
=======
            user = form.save(commit=False)
            user.email = request.POST.get("email_address")
            user.is_active = True
            user.save()

<<<<<<< HEAD
>>>>>>> 355e08d (Login persistence working + private pages + admin corrections + user model changes + backend authadded + changes to settings)
=======
            verification_object = Verification()
            verification_object.verified = user
            verification_object.verifier = user
            verification_object.save()

>>>>>>> a84a86d (Fixing Request Authentication)
            # Add to Email table
            email = request.POST.get("email_address")
            emailObject = Email()
<<<<<<< HEAD
            emailObject.email_address = email
            emailObject.user = user
=======
            emailObject.primary_email = email
            emailObject.user_id = user_id
>>>>>>> 5af6993 (Fix edit)
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

            github = request.POST.get("github")
            if github and github != "":
                handleObject = Handle(
                    user=user, site=Site.objects.get(site_id="github"), handle=github
                )
                handleObject.save()

            x = request.POST.get("x")
            if x and x != "":
                handleObject = Handle(
                    user=user, site=Site.objects.get(site_id="x"), handle=x
                )
                handleObject.save()

            user = authenticate(
                username=email, password=request.POST.get("password_hash")
            )
            login(request, user)
            return redirect("verify_email")
        return render(
            request,
            "mentapp/sign_up.html",
            {
                "form": form,
            },
        )
    else:
        return render(request, "mentapp/sign_up.html")
>>>>>>> 48995dc (Added functionality to sign_up page)

<<<<<<< HEAD
<<<<<<< HEAD
def profile(request):
    template = loader.get_template('mentapp/profile.html')
<<<<<<< HEAD
<<<<<<< HEAD
=======
def login(request):
    template = loader.get_template('login/login.html')
>>>>>>> 755d62a (Configured formatting rules,)
=======
>>>>>>> f3a6090 (profile page)
=======

=======
@login_required
>>>>>>> b2672c3 (Login now required to access profile)
def profile(request):
    template = loader.get_template("mentapp/profile.html")
>>>>>>> fb1dd3d (all tables added)
    return HttpResponse(template.render())
=======
=======

def profile(request):
    template = loader.get_template("mentapp/profile.html")
>>>>>>> e58ea8e (Linked login page to the backend)
    return HttpResponse(template.render())



def reset(request):
    if request.method == "POST":
        email_address = request.POST.get("email")
        user = User.objects.get(email=email_address)
        current_site = get_current_site(request)
        subject = "Reset your password"
        message = render_to_string(
            "mentapp/reset_password_message.html",
            {
                "request": request,
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": email_verification_token.make_token(user),
            },
        )
        email = EmailMessage(
            subject, message, "notifications@kontinua.org", [email_address]
        )
        email.content_subtype = "html"
        email.send()
        return JsonResponse({"success": True})
    return render(request, "mentapp/reset.html")


def verify_reset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and email_verification_token.check_token(user, token):
        return redirect(f"/reset_password")
    else:
        messages.warning(request, "The link is invalid.")
    return render(request, "mentapp/verify_email_confirm.html")


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.get(email=email)
        new_password = request.POST.get("new_password")
        user.set_password(new_password)
        user.save()
        return JsonResponse({"success": True})
    else:
        return render(request, "mentapp/reset_password.html")


def customLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_verified:
            login(request, user)
            return redirect("main")
        elif user is not None and not user.is_verified:
            login(request, user)
            return redirect(f"/profile/{user.user_id}")
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

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

<<<<<<< HEAD
=======
=======
=======

>>>>>>> 1170c32 (Fixed the Default Routing)
=======

>>>>>>> 7badf9f (Support creation bug fix)
=======

>>>>>>> eddf42b (Support creation bug fix)
@mentor_req
>>>>>>> ccfcdc2 (Decorators n pages)
def main(request, volume_id=1):
    template = loader.get_template("mentapp/main.html")

    volumes = (
        Volume.objects.values_list("volume_id", flat=True)
        .distinct()
        .order_by("volume_id")
    )

    if volume_id:
        chapters = Chapter.objects.filter(volume__volume_id=volume_id).distinct()
    else:
        chapters = []

    chapter_locs = Chapter_Loc.objects.filter(
        chapter__chapter_id__in=chapters
    ).distinct()

    context = {
        "volumes": volumes,
        "chapters": chapters,
        "volume_id": volume_id,
        "chapter_locs": chapter_locs,
    }

    return HttpResponse(template.render(context, request))


def chapter(request, volume_id, chapter_id):
    volume_id = get_object_or_404(Volume, volume_id=volume_id)
    chapter_id = get_object_or_404(Chapter, chapter_id=chapter_id)
    try:
        chapter_loc = Chapter_Loc.objects.get(chapter=chapter_id)
        title = chapter_loc.title
    except Chapter_Loc.DoesNotExist:
        title = None
    try:
        quizzes = Quiz.objects.filter(chapter=chapter_id, volume=volume_id)
    except Quiz.DoesNotExist:
        quizzes = None

    if request.method == "POST" and "makeNewQuiz" in request.POST:
        quizObject = Quiz()
        quizObject.conceptual_difficulty = 0
        quizObject.time_required_mins = 0
        quizObject.volume = volume_id
        quizObject.chapter = chapter_id
        quizObject.save()
        quiz_id = quizObject.quiz_id
        return redirect(f"../../../edit_quiz/{quiz_id}")

    return render(
        request,
        "mentapp/chapter.html",
        {
            "volume": volume_id,
            "chapter": chapter_id,
            "title": title,
            "quizzes": quizzes,
        },
    )

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 17adf3a (Implemented the Chapter Page with Quiz Information)

=======
=======

>>>>>>> 1170c32 (Fixed the Default Routing)
=======

>>>>>>> 7badf9f (Support creation bug fix)
=======

>>>>>>> eddf42b (Support creation bug fix)
@mentor_req
>>>>>>> ccfcdc2 (Decorators n pages)
def quiz(request, volume_id, chapter_id, quiz_id):
    volume_id = get_object_or_404(Volume, volume_id=volume_id)
    chapter_id = get_object_or_404(Chapter, chapter_id=chapter_id)
    quiz_id = get_object_or_404(Quiz, quiz_id=quiz_id)

    if request.method == "POST":
        if request.POST.get("command") == "viewer_publish":
            feedback = Quiz_Feedback()
            feedback.quiz = quiz_id
            feedback.creator_id = quiz_id.creator_id
            feedback.viewer_id = request.user

            feedback.challenge_rating = int(request.POST.get("challenge_rating"))
            feedback.time_rating = int(request.POST.get("time_rating"))
            feedback.viewer_comment = request.POST.get("viewer_comment")
            feedback.save()
            return JsonResponse({"success": True})
        elif request.POST.get("command") == "delete":
            feedback = Quiz_Feedback.objects.get(
                quiz=quiz_id,
                feedback_id=request.POST.get("feedback_id"),
            )
            feedback.delete()
            return JsonResponse({"success": True})
    else:
        avg_rating = quiz_id.conceptual_difficulty
        avg_time = quiz_id.time_required_mins

        try:
            reviews = []
            review_objects = Quiz_Feedback.objects.filter(
                quiz=quiz_id,
                date_completed__isnull=True,
            ).distinct()

            challenge_ratings = 0
            time_ratings = 0

            for review in review_objects:
                challenge_ratings += review.challenge_rating
                time_ratings += review.time_rating
                email = Email.objects.get(user=review.viewer_id, is_primary=True)
                reviews.append([email, review])

            if len(review_objects) > 1:
                avg_rating = challenge_ratings / len(review_objects)
                avg_time = time_ratings / len(review_objects)
        except:
            reviews = []

        creator = User()
        creator_email = Email()
        try:
            creator = User.objects.get(user_id=quiz_id.creator_id.user_id)
            creator_email = Email.objects.get(user=creator, is_primary=True)
        except (
            User.DoesNotExist,
            Email.DoesNotExist,
            User.DoesNotExist,
            AttributeError,
        ) as error:
            pass

        return render(
            request,
            "mentapp/quiz.html",
            {
                "volume": volume_id,
                "chapter": chapter_id,
                "quiz": quiz_id,
                "reviews": reviews,
                "creator": creator_email,
                "avg_rating": int(avg_rating),
                "avg_time": int(avg_time),
            },
        )


@quizmaker_req
def quiz_maker_view(request, volume_id, chapter_id, quiz_id):
    volume_id = get_object_or_404(Volume, volume_id=volume_id)
    chapter_id = get_object_or_404(Chapter, chapter_id=chapter_id)
    quiz_id = get_object_or_404(Quiz, quiz_id=quiz_id)

    if request.method == "POST":
        feedback = Quiz_Feedback.objects.get(
            quiz=quiz_id,
            feedback_id=request.POST.get("feedback_id"),
        )
        if request.POST.get("command") == "resolve":
            feedback.date_completed = date.today()
            feedback.save()
        elif request.POST.get("command") == "delete":
            feedback.delete()
        elif request.POST.get("command") == "publish":
            feedback.creator_comment = request.POST.get("creator_comment")
            feedback.save()
        return JsonResponse({"success": True})
    else:
        avg_rating = quiz_id.conceptual_difficulty
        avg_time = quiz_id.time_required_mins

        try:
            reviews = []
            review_objects = Quiz_Feedback.objects.filter(
                quiz=quiz_id,
                date_completed__isnull=True,
            ).distinct()

            challenge_ratings = 0
            time_ratings = 0

            for review in review_objects:
                challenge_ratings += review.challenge_rating
                time_ratings += review.time_rating
                email = Email.objects.get(user=review.viewer_id, is_primary=True)
                reviews.append([email, review])

            avg_rating = challenge_ratings / len(review_objects)
            avg_time = time_ratings / len(review_objects)
        except:
            reviews = []

        creator = User.objects.get(user_id=quiz_id.creator_id.user_id)
        creator_email = Email.objects.get(user=creator, is_primary=True)

        return render(
            request,
            "mentapp/quiz_maker_view.html",
            {
                "volume": volume_id,
                "chapter": chapter_id,
                "quiz": quiz_id,
                "reviews": reviews,
                "creator": creator_email,
                "avg_rating": int(avg_rating),
                "avg_time": int(avg_time),
            },
        )


@quizmaker_req
def question_approval(request):
    if request.method == "POST":
        question = Question.objects.get(
            question_id=request.POST.get("question_id"),
        )
        question.approval_requested = False
        if request.POST.get("command") == "accept":
            question.approved = True
            question_loc = Question_Loc.objects.get(question=question)
            question_loc.date_approved = date.today()
            question_loc.approver = request.user
            question_loc.save()
        question.save()
        return JsonResponse({"success": True})

    try:
        question_locs = Question_Loc.objects.order_by("date_created")
        question_info = []

        for question_loc in question_locs:
            question = question_loc.question
            if question.approval_requested and not question.approved:
                question_info = [question, question_loc]
                break

        chapter_loc = Chapter_Loc.objects.get(chapter=question.chapter)
        question_info.append(chapter_loc)
    except:
        question_info = []

    return render(
        request,
        "mentapp/question_approval.html",
        {"question": question_info},
    )


@admin_req
def promotion(request):
    if request.method == "POST":
        email_object = Email.objects.get(
            email_address=request.POST.get("email"), is_primary=True
        )
        user = email_object.user

        if request.POST.get("command") == "promote":
            if user.is_active == True:
                if user.is_quizmaker == True:
                    user.is_admin = True
                elif user.is_verified == True:
                    user.is_quizmaker = True
                elif user.is_verified == False:
                    user.is_verified = True

        user.promotion_requested = False
        user.save()

        verification_object = Verification.objects.get(verified=user)
        verification_object.verifier = request.user
        verification_object.save()
        return JsonResponse({"success": True})
    else:
        return render(
            request,
            "mentapp/promotion.html",
            {
                "newbies": grab_users(False, False, False, True, True),
                "mentors": grab_users(True, False, False, True, True),
                "quiz_makers": grab_users(True, True, False, True, True),
            },
        )


@admin_req
def user_directory(request):
    if request.method == "POST":
        email_object = Email.objects.get(
            email_address=request.POST.get("email"), is_primary=True
        )
        user = email_object.user
        status = "Newbie"
        color = "btn btn-outline-secondary"

        if request.POST.get("command") == "demote":
            if user.is_active == True:
                if user.is_admin == True:
                    user.is_admin = False
                    status = "Quiz Maker"
                    color = "btn btn-outline-warning"
                elif user.is_quizmaker == True:
                    user.is_quizmaker = False
                    status = "Mentor"
                    color = "btn btn-outline-info"
                elif user.is_verified == True:
                    user.is_verified = False
        else:
            user.is_active = False

        user.save()

        verification_object = Verification.objects.get(verified=user)
        verification_object.verifier = request.user
        verification_object.save()

        return JsonResponse({"success": True, "status": status, "color": color})
    else:
        return render(
            request,
            "mentapp/user_directory.html",
            {
                "newbies": grab_users(False, False, False, True, False),
                "mentors": grab_users(True, False, False, True, False),
                "quiz_makers": grab_users(True, True, False, True, False),
                "admins": grab_users(True, True, True, True, False),
            },
        )


def grab_users(verified, quiz_maker, admin, active, get_promotion):
    try:
        user_ids = (
            User.objects.filter(
                is_verified=verified,
                is_quizmaker=quiz_maker,
                is_admin=admin,
                is_active=active,
                promotion_requested=get_promotion,
            )
            .values_list("user_id", flat=True)
            .distinct()
        )
        users = grab_verification_info(user_ids)
    except:
        users = []

    return users


def grab_verification_info(user_ids):
    verification_info = []
    for user_id in user_ids:
        user = User.objects.get(user_id=user_id)
        email = Email.objects.get(user=user, is_primary=True)
        try:
            verifications = Verification.objects.get(verified=user)

            if verifications.verifier != verifications.verified:
                verifier_email = Email.objects.get(
                    user=verifications.verifier, is_primary=True
                )
                verification_info.append(
                    (
                        user_id,
                        email.email_address,
                        verifications.verifier.full_name,
                        verifier_email.email_address,
                    )
                )
            else:
                verification_info.append(
                    (
                        user_id,
                        email.email_address,
                        "",
                        "",
                    )
                )
        except Verification.DoesNotExist:
            verification_info.append((user_id, email.email_address))
    return verification_info


@login_required
def user_info(request, user_id):
    user = request.user
    if request.method == "POST":
        user.promotion_requested = True
        user.save()

        verification_object = Verification.objects.get(verified=user)
        verification_object.date_requested = date.today()
        verification_object.save()
        return JsonResponse({"success": True})

    if user_id != user.user_id and user.is_admin != True:
        return render(request, "mentapp/login.html")
    user_profile = get_object_or_404(User, user_id=user_id)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    return render(request, 'mentapp/profile.html', {'user_profile': user_profile})
>>>>>>> 91d40a5 (Able to populate fields from db)
=======
    email = get_object_or_404(Email, user_id=user_id)
<<<<<<< HEAD
    return render(request, 'mentapp/profile.html', {'user_profile': user_profile,
                                                    'email': email})
>>>>>>> e6150ad (All profile fields populated)
=======
=======
    email = get_object_or_404(Email, user_id=user_id, is_primary=True)
>>>>>>> 48995dc (Added functionality to sign_up page)
=======
=======
=======
    if user_profile.is_admin == True:
<<<<<<< HEAD
<<<<<<< HEAD
        return HttpResponseForbidden("Forbidden: Admin's use admin portal")
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 73d68a9 (added handling so admin can't login through normal forcing to use admin portal)
    print("This is the user_id:", user_id)
    print("This is the user retrieved", user_profile)
    print("This is the user associated email", user_profile.email)
>>>>>>> 355e08d (Login persistence working + private pages + admin corrections + user model changes + backend authadded + changes to settings)
=======
>>>>>>> 949f602 (Removed debugging statements)
=======
=======
        return redirect('/admin/')
>>>>>>> 7ea149b (Changes for routing)
=======
        return redirect("/admin/")
>>>>>>> f4d4c28 (Fix Editing Primary Email)

>>>>>>> a84a86d (Fixing Request Authentication)
    try:
        email = Email.objects.get(user=user_profile, is_primary=True)
        other_emails = Email.objects.filter(user=user_profile, is_primary=False)
        other_emailss = [obj.email_address for obj in other_emails]
<<<<<<< HEAD
        other_email = ', '.join(other_emailss)
<<<<<<< HEAD
<<<<<<< HEAD
=======
        print("THIS IS OTHER EMAILS", other_email)
>>>>>>> 3a78790 (Added loading of other emails)
=======
>>>>>>> fdab078 (Everything working now in the edit page)
=======
        other_email = ", ".join(other_emailss)
>>>>>>> 80ea2b4 (Fixed sign_up page to match new attribute names)
    except Email.DoesNotExist:
        email = None
<<<<<<< HEAD
>>>>>>> e153f37 (Edit profile page)
=======
    handles = Handle.objects.filter(user=user_profile)
<<<<<<< HEAD
>>>>>>> 93564c2 (Handles saved in database, displayed on profile page)
=======
    request_btn = "Request Authorization"

    if user.is_verified:
        request_btn = "Request Promotion"

>>>>>>> a84a86d (Fixing Request Authentication)
    return render(
        request,
        "mentapp/profile.html",
        {
            "user_profile": user_profile,
            "email": email,
            "other_email": other_email,
            "handles": handles,
            "request_btn": request_btn,
        },
    )
<<<<<<< HEAD
>>>>>>> e58ea8e (Linked login page to the backend)
=======


def user_edit(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    # print("user items", user)
    # print("request items", request.POST)
    for key, value in request.POST.items():
        # print("KEY", key, "VALUE", value)
        if key == "primary_email":
            Email.objects.filter(user_id=user_id, is_primary = True).update(email_address=value)
        if key == "other_emails":
            Email.objects.filter(user_id=user_id, is_primary = False).delete()
            insEmails = value.split(',')
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


def grab_questions_data_table(questions):
    questions_list = list()
    for question in questions:
        question_Loc = (
        # Display question only with ENG lang code and US dialect code for editing 
        Question_Loc.objects.get(
            question = question.question_id, lang_code="ENG", dialect_code="US"
        ))
        question_attachments = Question_Attachment.objects.filter(question = question_Loc)

        attachment_urls = list()
        for question_attachment in question_attachments:
            attachment_url = question_attachment.blob_key.file.url
            attachment_urls.append(attachment_url)

        question_values = dict()
        question_values["question_id"] = question.question_id
        question_values["chapter"] = question.chapter.chapter_id
        question_values["volume"] = question.chapter.volume.volume_id

        if question.creator is not None:
            question_values["creator"] = question_Loc.creator.full_name
        else:
            question_values["creator"] = ""

        question_values["conceptual_difficulty"] = question.conceptual_difficulty
        question_values["time_required_mins"] = question.time_required_mins
        question_values["point_value"] = question.point_value
        question_values["question_latex"] = question_Loc.question_latex
        question_values["attachment_urls"] = attachment_urls
        questions_list.append(question_values)
    return questions_list

def grab_quiz_questions_data_table(quiz_questions):
    questions = list()
    for quiz_question in quiz_questions:
        questions.append(quiz_question.question)

    questionTable = grab_questions_data_table(questions)
    for question_values, quiz_question in zip(questionTable, quiz_questions):
        question_values["ordering"] = quiz_question.ordering
    
    return questionTable


def grab_questions_data_table(questions):
    questions_list = list()
    for question in questions:
        question_Loc = (
            # Display question only with ENG lang code and US dialect code for editing
            Question_Loc.objects.get(
                question=question.question_id, lang_code="ENG", dialect_code="US"
            )
        )
        question_attachments = Question_Attachment.objects.filter(question=question_Loc)

        attachment_urls = list()
        for question_attachment in question_attachments:
            attachment_url = question_attachment.blob_key.file.url
            attachment_urls.append(attachment_url)

        question_values = dict()
        question_values["question_id"] = question.question_id
        question_values["chapter"] = question.chapter.chapter_id
        question_values["volume"] = question.chapter.volume.volume_id

        if question.creator is not None:
            question_values["creator"] = question_Loc.creator.full_name
        else:
            question_values["creator"] = ""

        question_values["conceptual_difficulty"] = question.conceptual_difficulty
        question_values["time_required_mins"] = question.time_required_mins
        question_values["point_value"] = question.point_value
        question_values["question_latex"] = question_Loc.question_latex
        question_values["attachment_urls"] = attachment_urls
        questions_list.append(question_values)
    return questions_list


def grab_quiz_questions_data_table(quiz_questions):
    questions = list()
    for quiz_question in quiz_questions:
        questions.append(quiz_question.question)

    questionTable = grab_questions_data_table(questions)
    for question_values, quiz_question in zip(questionTable, quiz_questions):
        question_values["ordering"] = quiz_question.ordering

    return questionTable


@login_required
@quizmaker_req
def edit_quiz(request, quiz_id):
    quiz_instance = get_object_or_404(Quiz, quiz_id=quiz_id)
    quiz_questions = (
        Quiz_Question.objects.all()
        .filter(quiz=quiz_instance.quiz_id)
        .order_by("ordering")
    )
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    questions_Loc_quiz_attatchments = list()

    for quiz_question in quiz_questions:
        # Display question only with ENG lang code and US dialect code for editing
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        question_Loc = Question_Loc.objects.all().filter(
=======
        questions_Loc_local = Question_Loc.objects.all().filter(
>>>>>>> f775257 (Initial changes for pdf rendering)
=======
        questions_Loc = Question_Loc.objects.all().filter(
>>>>>>> 32653f4 (Added Texlive distribution)
            question=quiz_question.question,
            lang_code="ENG",
            dialect_code="US",
        ).first()
=======
        questions_Loc = (
            Question_Loc.objects.all()
            .filter(
                question=quiz_question.question,
                lang_code="ENG",
                dialect_code="US",
            )
            .first()
        )
>>>>>>> 7e40b51 (Download functionality to chapter page)

<<<<<<< HEAD
        question_attachments = Question_Attachment.objects.filter(question=question_Loc)
=======
        question_attachments = Question_Attachment.objects.filter(
            question=questions_Loc
        )
>>>>>>> 32653f4 (Added Texlive distribution)

        files = list()
        for question_attachment in question_attachments:
            file = question_attachment.blob_key.file
            files.append(file)

<<<<<<< HEAD
        questions_Loc_quiz_attatchments.append((question_Loc, quiz_question, files))
=======
        questions_Loc_quiz_attatchments.append((questions_Loc, quiz_question, files))
>>>>>>> 32653f4 (Added Texlive distribution)

=======
>>>>>>> 1c5155a (JavaScript rewrite for editing quizzes, Quiz Label, LaTeX image support with URL (implemented edit_quiz and associated add_question and add_support pages))
=======
>>>>>>> a8bcbf5 (JavaScript rewrite for editing quizzes, Quiz Label, LaTeX image support with URL (implemented edit_quiz and associated add_question and add_support pages))
=======
=======
>>>>>>> e5d8588 (Support rendering for PDFs)
    quiz_supports = (
        Quiz_Support.objects.all()
        .filter(quiz=quiz_instance.quiz_id)
        .order_by("ordering")
    )

<<<<<<< HEAD
>>>>>>> 3cf110b (Support rendering for PDFs)
=======
>>>>>>> e5d8588 (Support rendering for PDFs)
    if request.method == "POST":
        if request.POST.get("command") == "save":
            # TODO: Ids are just the questions, update edit_quiz.html to include supports
            ids_str = json.loads(request.POST.get("ids"))
            ids = list()
            for id_str in ids_str:
                ids.append(int(id_str))

            for question in quiz_questions:
                if question.question not in ids:
                    question.delete()

            for count, id in enumerate(ids):
                for quiz_question in quiz_questions:
                    if quiz_question.question.question_id == id:
                        quiz_question.ordering = count
                        quiz_question.save()
            quiz_instance.label = request.POST.get("label")
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            print(request.POST.get("label"))
=======
>>>>>>> 2504016 (Linux Tex-Live distribution)
=======
>>>>>>> 32cac51 (Associated Quiz Feedback to Quiz instead of Rendering)
            quiz_instance.conceptual_difficulty = float(
                request.POST.get("conceptual_difficulty")
            )
            quiz_instance.time_required_mins = int(
                request.POST.get("time_required_mins")
            )
            quiz_instance.volume = get_object_or_404(
                Volume, volume_id=request.POST.get("volume")
            )
            quiz_instance.chapter = get_object_or_404(
                Chapter, chapter_id=request.POST.get("chapter")
            )
<<<<<<< HEAD
<<<<<<< HEAD
=======
            quiz_instance.conceptual_difficulty = float(request.POST.get("conceptual_difficulty"))
            quiz_instance.time_required_mins = int(request.POST.get("time_required_mins"))
            quiz_instance.volume = get_object_or_404(Volume, volume_id = request.POST.get("volume"))    
            quiz_instance.chapter = get_object_or_404(Chapter, chapter_id = request.POST.get("chapter"))
>>>>>>> 66d0926 (Removed log and print statements, fixed quiz name in chapter.html)
=======
>>>>>>> 2504016 (Linux Tex-Live distribution)
=======
>>>>>>> 32cac51 (Associated Quiz Feedback to Quiz instead of Rendering)
            calculator_allowed_str = request.POST.get("calculator_allowed")
            computer_allowed_str = request.POST.get("computer_allowed")
            internet_allowed_str = request.POST.get("internet_allowed")
            book_allowed_str = request.POST.get("book_allowed")

            if calculator_allowed_str == "true":
                quiz_instance.calculator_allowed = True
            else:
                quiz_instance.calculator_allowed = False

            if computer_allowed_str == "true":
                quiz_instance.computer_allowed = True
            else:
                quiz_instance.computer_allowed = False

            if internet_allowed_str == "true":
                quiz_instance.internet_allowed = True
            else:
                quiz_instance.internet_allowed = False

            if book_allowed_str == "true":
                quiz_instance.book_allowed = True
            else:
                quiz_instance.book_allowed = False

            quiz_instance.save()
            question_list = []
            support_list = []

            for id in ids:
                for quiz_question in quiz_questions:
                    if quiz_question.question.question_id == id:
                        question_meta = quiz_question.question
                        question_content = get_object_or_404(
                            Question_Loc, question=question_meta
                        )
                        question_list.append(question_content)
                for quiz_support in quiz_supports:
                    if quiz_support.support.support_id == id:
                        support_meta = quiz_support.support
                        support_content = get_object_or_404(
                            Support_Loc, support=support_meta
                        )
                        support_list.append(support_content)

            #latex_to_pdf(question_list, support_list, quiz_instance)
            return JsonResponse({"success": True})
    else:
        if request.GET.get("command") == "fetch_quiz_questions":
            return JsonResponse(
                grab_quiz_questions_data_table(quiz_questions), safe=False
            )

    chapters = Chapter.objects.all()
    volumes = Volume.objects.all()
    return render(
        request,
        "mentapp/edit_quiz.html",
        {"quiz_instance": quiz_instance, "volumes": volumes, "chapters": chapters},
    )


def edit_quiz_add_question(request, quiz_id):
    questions_Locs = Question_Loc.objects.all()
    chapters = Chapter.objects.all()
    volumes = Volume.objects.all()
    creators = User.objects.all()

    if request.method == "POST":
        quiz_instance = get_object_or_404(Quiz, quiz_id=quiz_id)
        if request.POST.get("command") == "save_changes":
            quiz_questions = (
                Quiz_Question.objects.all().filter(quiz=quiz_id).order_by("ordering")
            )
            questions_to_add_id_str = json.loads(
                request.POST.get("questions_to_add_ids")
            )
            quiz_questions = (
                Quiz_Question.objects.all().filter(quiz=quiz_id).order_by("ordering")
            )
            questions_to_add_id_str = json.loads(
                request.POST.get("questions_to_add_ids")
            )

            for question_id in questions_to_add_id_str:
                if quiz_questions.filter(question_id=question_id).count() == 0:
                    question_instance = get_object_or_404(
                        Question, question_id=question_id
                    )
                    Quiz_Question.objects.create(
                        quiz=quiz_instance,
                        question=question_instance,
                        ordering=quiz_questions.count(),
                    )
            return JsonResponse({"success": True})
    elif request.method == "GET" and request.GET.get("command") == "filter":
        chapter_filter = request.GET.get("chapter")
        creator_filter = request.GET.get("creator")
        volume_filter = request.GET.get("volume")
        point_filter = request.GET.get("point")
        time_filter = request.GET.get("time")
        difficulty_filter = request.GET.get("difficulty")
<<<<<<< HEAD
<<<<<<< HEAD
        question_instances = Question.objects.all()
        chapter_filter = request.GET.get("chapter")
        creator_filter = request.GET.get("creator")
        volume_filter = request.GET.get("volume")
        point_filter = request.GET.get("point")
        time_filter = request.GET.get("time")
        difficulty_filter = request.GET.get("difficulty")
        question_instances = Question.objects.all()
=======
        question_instances = Question.objects.all().filter(approved=True)
>>>>>>> b3d4630 (Fixed Question Bank)
=======
        question_instances = Question.objects.all()
<<<<<<< HEAD
        #TODO fix question approval
        #question_instances = Question.objects.all().filter(approved=True)
>>>>>>> a943d23 (LaTeX macro ready, times out when saving due to pdf generation)
=======
        # TODO fix question approval
        # question_instances = Question.objects.all().filter(approved=True)
>>>>>>> f4d4c28 (Fix Editing Primary Email)

        if volume_filter:
            question_instances = question_instances.filter(
                chapter__volume__volume_id=volume_filter
            )
<<<<<<< HEAD
<<<<<<< HEAD
        if volume_filter:
            question_instances = question_instances.filter(
                chapter__volume__volume_id=volume_filter
            )

        if chapter_filter:
            question_instances = question_instances.filter(chapter=chapter_filter)
=======

>>>>>>> 1c5155a (JavaScript rewrite for editing quizzes, Quiz Label, LaTeX image support with URL (implemented edit_quiz and associated add_question and add_support pages))
=======

>>>>>>> a8bcbf5 (JavaScript rewrite for editing quizzes, Quiz Label, LaTeX image support with URL (implemented edit_quiz and associated add_question and add_support pages))
        if chapter_filter:
            question_instances = question_instances.filter(chapter=chapter_filter)

        if creator_filter:
            question_instances = question_instances.filter(creator=creator_filter)

        if point_filter:
            question_instances = question_instances.filter(point_value=point_filter)
        if creator_filter:
            question_instances = question_instances.filter(creator=creator_filter)

        if point_filter:
            question_instances = question_instances.filter(point_value=point_filter)

        if difficulty_filter:
            question_instances = question_instances.filter(
                conceptual_difficulty=difficulty_filter
            )
        if difficulty_filter:
            question_instances = question_instances.filter(
                conceptual_difficulty=difficulty_filter
            )

        if time_filter:
            question_instances = question_instances.filter(
                time_required_mins=time_filter
            )
        if time_filter:
            question_instances = question_instances.filter(
                time_required_mins=time_filter
            )

<<<<<<< HEAD
<<<<<<< HEAD
        questions_list = list()

        for question in question_instances:
            question_Loc = (
                # Display question only with ENG lang code and US dialect code for editing
<<<<<<< HEAD
=======
                Question_Loc.objects.all()
                .filter(
                    lang_code="ENG", dialect_code="US", question=question.question_id
                )
                .first()
            )
            question_values = dict()
            question_values["question_id"] = question.question_id
        questions_list = list()
        for question in question_instances:
            question_Loc = (
>>>>>>> f775257 (Initial changes for pdf rendering)
                Question_Loc.objects.all()
                .filter(
                    lang_code="ENG", dialect_code="US", question=question.question_id
                )
                .first()
            )

            question_attachments = Question_Attachment.objects.filter(
                question=question_Loc
            )

            attachment_urls = list()
            for question_attachment in question_attachments:
                attachment_url = question_attachment.blob_key.file.url
                attachment_urls.append(attachment_url)

            question_values = dict()
            question_values["question_id"] = question.question_id

            if question.chapter is not None:
                question_values["chapter"] = question.chapter.chapter_id
                question_values["volume"] = question.chapter.volume.volume_id
            else:
                question_values["chapter"] = ""
                question_values["volume"] = ""

            if question.creator is not None:
                question_values["creator"] = question_Loc.creator.full_name
            else:
                question_values["creator"] = ""
            if question.chapter is not None:
                question_values["chapter"] = question.chapter.chapter_id
                question_values["volume"] = question.chapter.volume.volume_id
            else:
                question_values["chapter"] = ""
                question_values["volume"] = ""

            if question.creator is not None:
                question_values["creator"] = question_Loc.creator.full_name
            else:
                question_values["creator"] = ""

            question_values["conceptual_difficulty"] = question.conceptual_difficulty
            question_values["time_required_mins"] = question.time_required_mins
            question_values["point_value"] = question.point_value
            question_values["question_latex"] = question_Loc.question_latex
            question_values["attachment_urls"] = attachment_urls
            questions_list.append(question_values)
        return JsonResponse(questions_list, safe=False)
=======
        return JsonResponse(grab_questions_data_table(question_instances), safe=False)
>>>>>>> 1c5155a (JavaScript rewrite for editing quizzes, Quiz Label, LaTeX image support with URL (implemented edit_quiz and associated add_question and add_support pages))
=======
        return JsonResponse(grab_questions_data_table(question_instances), safe=False)
>>>>>>> a8bcbf5 (JavaScript rewrite for editing quizzes, Quiz Label, LaTeX image support with URL (implemented edit_quiz and associated add_question and add_support pages))

    return render(
        request,
        "mentapp/edit_quiz_add_question.html/",
        {
            "quiz_id": quiz_id,
            "quiz_id": quiz_id,
            "questions_Locs": questions_Locs,
            "chapters": chapters,
            "volumes": volumes,
            "creators": creators,
        },
    )


def edit_quiz_add_support(request, quiz_id):

    support_Locs = Support_Loc.objects.all()
    volumes = Volume.objects.all()
    creators = User.objects.all()

    if request.method == "POST":
        quiz_instance = get_object_or_404(Quiz, quiz_id=quiz_id)
        if request.POST.get("command") == "save_changes":
            quiz_supports = (
                Quiz_Support.objects.all().filter(quiz=quiz_id).order_by("ordering")
            )
            supports_to_add_id_str = json.loads(request.POST.get("supports_to_add_ids"))

            for support_id in supports_to_add_id_str:
                if quiz_supports.filter(support_id=support_id).count() == 0:
                    support_instance = get_object_or_404(Support, support_id=support_id)
                    Quiz_Support.objects.create(
                        quiz=quiz_instance,
                        support=support_instance,
                        ordering=quiz_supports.count(),
                    )

            return JsonResponse({"success": True})
    elif request.method == "GET" and request.GET.get("command") == "filter":
        creator_filter = request.GET.get("creator")
        volume_filter = request.GET.get("volume")
        title_filter = request.GET.get("title")
        support_instances = Support_Loc.objects.all()

        if volume_filter:
            support_instances = support_instances.filter(
                support__volume_id__volume_id=volume_filter
            )

        if creator_filter:
            support_instances = support_instances.filter(creator=creator_filter)

        if title_filter:
            support_instances = support_instances.filter(title=title_filter)

        supports_list = list()

        for support in support_instances:
            support_Loc = (
                # Display question only with ENG lang code and US dialect code for editing
                Support_Loc.objects.all()
                .filter(lang_code="ENG", dialect_code="US", support=support.support)
                .first()
            )

            support_attachments = Support_Attachment.objects.filter(support=support_Loc)

            attachment_urls = list()
            for support_attachment in support_attachments:
                attachment_url = support_attachment.blob_key.file.url
                attachment_urls.append(attachment_url)

            support_values = dict()
            support_values["support_id"] = support.support_id

            if support.support.volume_id.volume_id is not None:
                support_values["volume"] = support.support.volume_id.volume_id
            else:
                support_values["volume"] = ""

            if support.title is not None:
                support_values["title"] = support.title
            else:
                support_values["title"] = ""

            if support.creator is not None:
                support_values["creator"] = support_Loc.creator.full_name
            else:
                support_values["creator"] = ""

            support_values["support_latex"] = support_Loc.content_latex
            support_values["attachment_urls"] = attachment_urls
            supports_list.append(support_values)
        return JsonResponse(supports_list, safe=False)

    return render(
        request,
        "mentapp/edit_quiz_add_support.html/",
        {
            "quiz_id": quiz_id,
            "questions_Locs": support_Locs,
            "volumes": volumes,
            "creators": creators,
        },
    )


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 0f14dbf (view supports)
def header(request, page):
=======
def header(request):
>>>>>>> ea0afb2 (Update views.py)
=======
def header(request):
>>>>>>> c2e8da3 (header)
    return render(
        request,
        "mentapp/header.html",
    )


def footer(request):
    return render(
        request,
        "mentapp/footer.html",
    )


def user_edit(request, user_id):
    user = get_object_or_404(User, user_id=user_id)

    for key, value in request.POST.items():
        if key == "primary_email":
            Email.objects.filter(user=user, is_primary=True).delete()

            emailObject = Email()
            emailObject.email_address = value
            emailObject.user = user
            emailObject.is_primary = True
            emailObject.is_verified = True
            emailObject.save()
        if key == "other_emails":
            Email.objects.filter(user=user, is_primary=False).delete()
            insEmails = value.split(",")
            for em in insEmails:
                emailObject = Email()
                emailObject.email_address = em
<<<<<<< HEAD
                emailObject.user_id = user
=======
                emailObject.user = user
>>>>>>> eb9254f (Working but still instantiating + fixed a random big on saving changed user stuff)
                emailObject.save()
        # Check if the user object has this field and the value is not empty
        if hasattr(user, key) and value.strip():
            setattr(user, key, value)
    user.save()
    return redirect(f"/profile/{user.user_id}")


<<<<<<< HEAD
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 0b5462f (Implemented Request Translation Email Notification)
=======
    try:
        email = Email.objects.get(user_id=user_id)
    except Email.DoesNotExist:
        email = None
    return render(
        request, "mentapp/profile.html", {"user_profile": user_profile, "email": email}
    )
>>>>>>> fb1dd3d (all tables added)
=======

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






>>>>>>> 7fc2710 (main page volume + chapter selector)
=======
>>>>>>> 17adf3a (Implemented the Chapter Page with Quiz Information)
=======
    
>>>>>>> dc9408a (update)
=======
=======
def verify_email(request):
    if request.method == "POST":
        email_address = request.user.email
        email_object = Email.objects.get(email_address=email_address)

        if not email_object.is_verified:
            current_site = get_current_site(request)
            user = request.user
            subject = "Verify Email"
            message = render_to_string(
                "mentapp/verify_email_message.html",
                {
                    "request": request,
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": email_verification_token.make_token(user),
                },
            )
            email = EmailMessage(
                subject, message, "notifications@kontinua.org", [email_address]
            )
            email.content_subtype = "html"
            email.send()
            return JsonResponse({"success": True})
        else:
            return redirect("sign_up")
    return render(request, "mentapp/verify_email.html")


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and email_verification_token.check_token(user, token):
        email = user.email
        email_object = Email.objects.get(email_address=email)
        email_object.is_verified = True
        email_object.save()
        messages.success(request, "Your email has been verified.")
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("user_info", user_id=user.user_id)
    else:
        messages.warning(request, "The link is invalid.")
    return render(request, "mentapp/verify_email_confirm.html")


# def request_translation(request, user_id):
#     # need to verify email to ses when they sign up in order for this to work
#     email = get_object_or_404(Email, user_id=user_id, is_primary=True)
#     primary_language = get_object_or_404(User.primary_language, user_id=user_id)
#     send_mail(
#         "Kontinua Quiz Questions Translations Request",
#         "Hi there! We have noticed you are fluent in "
#         + primary_language
#         + ". This week these questions were added in "
#         + primary_language
#         + ". I can do a preliminary translation to "
#         + primary_language
#         + " using Google Translate. Would you look at and correct those preliminary translations?  Click here.",
#         "notifications@kontinua.org",
#         [email],
#     )
>>>>>>> e5984d8 (Implement Email Verification & Password Reset)


def download_pdf(request, quiz_id):
    quiz_instance = get_object_or_404(Quiz, quiz_id=quiz_id)
    try:
        quiz_rendering_instance = Quiz_Rendering.objects.filter(
            quiz=quiz_instance
        ).latest("date_created")
    except:
        # function that saves the PDF
        question_list = []
        support_list = []

        quiz_question_list = Quiz_Question.objects.filter(quiz=quiz_instance)
        for quiz_question in quiz_question_list:
            question_meta = quiz_question.question
            question_content = get_object_or_404(Question_Loc, question=question_meta)
            question_list.append(question_content)

        quiz_support_list = Quiz_Support.objects.filter(quiz=quiz_instance)
        for quiz_support in quiz_support_list:
            support_meta = quiz_support.support
            support_content = get_object_or_404(Support_Loc, support=support_meta)
            support_list.append(support_content)
        try:
            latex_to_pdf(question_list, support_list, quiz_instance)
        except:
            raise SystemError
        return download_pdf(request, quiz_id)
    blob_instance = quiz_rendering_instance.blob_key

    response = HttpResponse(blob_instance.file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{blob_instance.filename}"'
    return response
<<<<<<< HEAD
>>>>>>> 906fe04 (download works)
=======


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 2889b3c (Download PDF bug fix)
def upload_pdf(request, pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_content = pdf_file.read()

        # Use Django's ContentFile to create a file-like object
        content_file = ContentFile(pdf_content, name=os.path.basename(pdf_path))

        blob_instance = Blob(
            file=content_file,
            content_type="application/pdf",
            filename=os.path.basename(pdf_path),
        )
        blob_instance.save()

        return JsonResponse(
            {"status": "success", "message": "File uploaded successfully"}
        )
    except Exception as e:
<<<<<<< HEAD
<<<<<<< HEAD
        return JsonResponse({'status': 'error', 'message': str(e)})
<<<<<<< HEAD
>>>>>>> 5eb3753 (upload pdfs)
=======
=======
        return JsonResponse({"status": "error", "message": str(e)})

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> c58b4ad (Initial changes for pdf rendering)
=======
>>>>>>> aabf7f6 (edit/delete quiz buttons)

=======
=======

>>>>>>> a84a86d (Fixing Request Authentication)
@quizmaker_req
>>>>>>> 8a330aa (Fixed bug just needed to protect create API instead of edit API)
def create_quiz(request, volume_id, chapter_id):
    if request.method == "POST":
        # Create a new Quiz instance
        quiz = Quiz.objects.create(
            conceptual_difficulty=1,
            time_required_mins=10,
            calculator_allowed=False,
            computer_allowed=False,
            internet_allowed=False,
            book_allowed=False,
            volume_id=volume_id,
            chapter_id=chapter_id,
            creator_id=request.user,
        )

        # Redirect to the edit page for the new quiz
<<<<<<< HEAD
<<<<<<< HEAD
        return redirect('/edit_quiz/{}'.format(quiz.quiz_id))
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> a206368 (Fixed styling and added more elements)
=======
        return JsonResponse({"status": "error", "message": str(e)})
<<<<<<< HEAD
>>>>>>> 981eeea (Submit questions to database)
=======
=======
    
=======
        return redirect("/edit_quiz/{}".format(quiz.quiz_id))


>>>>>>> 2889b3c (Download PDF bug fix)
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    url = request.path

    if request.method == "POST":
        quiz.delete()

<<<<<<< HEAD
>>>>>>> aabf7f6 (edit/delete quiz buttons)

def create_support(request):
=======
    

def create_support(request):
<<<<<<< HEAD

    form = LatexForm(request.POST)
>>>>>>> 324f15d (support view and url)
=======
>>>>>>> 441d01e (supports multiple attachments)
    
=======
        return redirect("/edit_quiz/{}".format(quiz.quiz_id))
=======
    return redirect(request.META.get("HTTP_REFERER", "/"))
>>>>>>> 2889b3c (Download PDF bug fix)


def latex_window_support(request, support_id, width):
    return render(
        request,
        "mentapp/latex_window.html",
        {"type": "support", "support_id": support_id, "width": width},
    )


def grab_attachments_support(support_id):
    support = get_object_or_404(Support, support_id=support_id)
    support_loc = get_object_or_404(
        Support_Loc, support=support, lang_code="ENG", dialect_code="US"
    )
    attachments = Support_Attachment.objects.filter(
        support=support_loc, lang_code="ENG", dialect_code="US"
    )
    attachmentsList = list()

    for attachment in attachments:
        attachmentDict = dict()
        attachmentDict["filename"] = attachment.filename
        attachmentDict["url"] = attachment.blob_key.file.url
        attachmentsList.append(attachmentDict)

    return attachmentsList


# Returns a JSON response with only the attachment files and names
def fetch_attachments_support(request, support_id):
    attachmentsList = grab_attachments_support(support_id)
    return JsonResponse({"attachments": attachmentsList})


# Returns a JSON response with the attachment files and names and the LaTeX
def fetch_attachments_inputs_support(request, support_id):
    support = get_object_or_404(Support, support_id=support_id)
    support_Loc = get_object_or_404(
        Support_Loc, support=support, lang_code="ENG", dialect_code="US"
    )
    input = support_Loc.content_latex
    attachmentsList = grab_attachments_support(support_id)
    return JsonResponse({"attachments": attachmentsList, "input": input})


def create_support(request, quiz_id):

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> c58b4ad (Initial changes for pdf rendering)
    volumes = (
        Volume.objects.values_list("volume_id", flat=True)
        .distinct()
        .order_by("volume_id")
    )
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> cbf594b (fixed creator/approver id)
    creators = (
        User.objects.values_list("user_id")
    )
=======
    creators = User.objects.values_list("user_id")
>>>>>>> c58b4ad (Initial changes for pdf rendering)
=======
>>>>>>> 7badf9f (Support creation bug fix)
=======
>>>>>>> eddf42b (Support creation bug fix)

    volume_id = 1

    if request.method == "POST":
        form = LatexForm(request.POST, request.FILES)
        support_content = request.POST.get("latex_support")
        support_title = request.POST.get("title")
        volume_id = int(request.POST.get("volume"))
        volume = get_object_or_404(Volume, volume_id=volume_id)
        support_attachments = request.FILES.getlist("attachments")

        if "submit-support" in request.POST:

            support = Support(volume_id=volume)
            support.save()
<<<<<<< HEAD
=======

    volume_id = 1

    if request.method == "POST":
        form = LatexForm(request.POST, request.FILES)
        support_content = request.POST.get("latex_support")
        support_title = request.POST.get("title")
        volume_id = int(request.POST.get("volume"))
        volume = get_object_or_404(Volume, volume_id=volume_id)
        support_attachments = request.FILES.getlist('attachments')
        print(support_attachments)

        

        if "submit-support" in request.POST:
            
            support = Support(volume_id = volume)
            support.save()
<<<<<<< HEAD
            print(support.volume_id)
>>>>>>> 324f15d (support view and url)
=======
>>>>>>> 441d01e (supports multiple attachments)
            
            support_loc = Support_Loc(
            support=support,
            title_latex=support_title,
            content_latex=support_content,
<<<<<<< HEAD
<<<<<<< HEAD
            creator_id=creators.first()[0],
            approver_id=creators.first()[0]
=======
            creator_id="e79c167f-6900-4525-9aa6-bd7263c1fbb3",
            approver_id="e79c167f-6900-4525-9aa6-bd7263c1fbb3"
>>>>>>> 324f15d (support view and url)
=======
            creator_id=creators.first()[0],
            approver_id=creators.first()[0]
>>>>>>> cbf594b (fixed creator/approver id)
=======

            support_loc = Support_Loc(
                support=support,
                title_latex=support_title,
                content_latex=support_content,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
                creator_id=creators.first()[0],
                approver_id=creators.first()[0],
>>>>>>> c58b4ad (Initial changes for pdf rendering)
=======
                creator=User.objects.distinct().first(),
                approver=User.objects.distinct().first(),
>>>>>>> 7badf9f (Support creation bug fix)
=======
                creator=User.objects.distinct().first(),
                approver=User.objects.distinct().first(),
>>>>>>> eddf42b (Support creation bug fix)
=======
                creator=request.user,
>>>>>>> de7f334 (Creator fields, no questions edge case, deleted imports)
            )

            support_loc.save()

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> c58b4ad (Initial changes for pdf rendering)
            for attachment in support_attachments:
=======
            support_attachments = request.FILES.getlist('attachments')

            for attachment in support_attachments:

>>>>>>> 324f15d (support view and url)
=======

            for attachment in support_attachments:
>>>>>>> 441d01e (supports multiple attachments)
                blob = Blob(
                    file=attachment,
                    content_type=attachment.content_type,
                    filename=attachment.name,
                )
                blob.save()

                support_attachment_instance = Support_Attachment(
<<<<<<< HEAD
<<<<<<< HEAD
                    support=support,
=======
                    support=support_loc,
>>>>>>> a98e60f (fix create support)
                    lang_code=support_loc.lang_code,
                    dialect_code=support_loc.dialect_code,
=======
                    support=support_loc,
                    lang_code = support_loc.lang_code,
                    dialect_code = support_loc.dialect_code,
>>>>>>> 8e5fc84 (Update views.py)
                    filename=blob.filename,
                    blob_key=blob,
                )
                support_attachment_instance.save()

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            return redirect('main')
            
=======
                return main(request)

>>>>>>> 324f15d (support view and url)
=======
            return redirect('main')
            
>>>>>>> 441d01e (supports multiple attachments)
=======
            return redirect("main")

>>>>>>> c58b4ad (Initial changes for pdf rendering)
        return render(
            request,
            "mentapp/create_support.html",
            {
                "form": form,
                "volumes": volumes,
<<<<<<< HEAD
<<<<<<< HEAD
                "volume_id": volume_id,
                "support_content": support_content,
<<<<<<< HEAD
=======
                "support_content": support_content
>>>>>>> 324f15d (support view and url)
=======
                "volume_id": volume_id,
                "support_content": support_content,
>>>>>>> 441d01e (supports multiple attachments)
                }
            )
=======
            },
        )
>>>>>>> c58b4ad (Initial changes for pdf rendering)
    else:
        return render(
            request,
            "mentapp/create_support.html",
<<<<<<< HEAD
            {
<<<<<<< HEAD
<<<<<<< HEAD
                "form": LatexForm(),
                "volumes": volumes
                }
            )
>>>>>>> 0e18c57 (add attachments and blobs to db)
=======
                "form": form,
                "volumes": volumes,
=======
                "form": LatexForm(),
                "volumes": volumes
>>>>>>> 441d01e (supports multiple attachments)
                }
            )
>>>>>>> 324f15d (support view and url)
=======
            {"form": LatexForm(), "volumes": volumes},
        )
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> c58b4ad (Initial changes for pdf rendering)
=======

def handles(request): 
    if request.method == 'POST':
        if request.POST.get("platform") == 'twitter':
            sitechoice = Site.objects.get(site_id=1)
        elif request.POST.get("platform") == 'instagram':
            sitechoice = Site.objects.get(site_id=2)
        elif request.POST.get("platform") == 'linkedin':
            sitechoice = Site.objects.get(site_id=3)
        elif request.POST.get("platform") == 'facebook':
            sitechoice = Site.objects.get(site_id=4)
        elif request.POST.get("platform") == 'github':
            sitechoice = Site.objects.get(site_id=5)
        elif request.POST.get("platform") == 'youtube':
            sitechoice = Site.objects.get(site_id=6)
        new_handle = Handle(
            site = sitechoice, 
            handle = request.POST.get("username"),
            user = request.user,
        )
        new_handle.save()
    user_handles = Handle.objects.filter(user=request.user)
    context = {'user_handles': user_handles}
<<<<<<< HEAD
<<<<<<< HEAD
    return render(request, 'mentapp/handles.html', context)
>>>>>>> f94ffd3 (Issues with model definitions)
=======
    print(context)
=======
>>>>>>> 918c9f6 (Removing print statements)
    return render(request, 'mentapp/handles.html', context)

def delete_handle(request, handle, site_id, user_id):
    curr_user = get_object_or_404(User, user_id=user_id)
    curr_site = get_object_or_404(Site, site_id=site_id)
    handle = get_object_or_404(Handle, handle=handle, site=curr_site, user=curr_user)
    if request.method == "POST":
        handle.delete()
    # Redirect to the referring page, or a default page if no referrer is found
    return redirect(request.META.get("HTTP_REFERER", "/"))
>>>>>>> 8faf4bf (Handles page done)
=======
=======
    if request.method == 'POST':
=======
    if request.method == "POST":
>>>>>>> a84a86d (Fixing Request Authentication)

        support = Support.objects.create(volume_id=Volume.objects.first())
        support_loc = Support_Loc.objects.create(support=support, title="")

        return redirect(f"/edit_support/{quiz_id}/{support.support_id}")

    return render(request, "mentapp/main.html")

def edit_support(request, quiz_id, support_id):
    support_object = get_object_or_404(Support, support_id=support_id)
    volumes = (
        Volume.objects.values_list("volume_id", flat=True)
        .distinct()
        .order_by("volume_id")
    )
    support_loc = get_object_or_404(Support_Loc, support=support_object)

    content = support_loc.content_latex
    title = support_loc.title
    volume_id = support_object.volume_id

    form = LatexForm(
        initial={
            "latex_support": content,
            "title": title,
            "volume": volume_id,
        }
    )

    if request.method == "POST":
        form = LatexForm(request.POST, request.FILES)
        support_content = request.POST.get("latex_support")
        support_title = request.POST.get("title")
        volume_id = int(request.POST.get("volume"))
        volume = get_object_or_404(Volume, volume_id=volume_id)
        support_attachments = request.FILES.getlist("attachments")

        if "submit-support" in request.POST:

            support_object.volume_id = volume
            support_object.save()

<<<<<<< HEAD
<<<<<<< HEAD
            support_loc.title_latex=support_title
            support_loc.content_latex=support_content
=======
            support_loc.title_latex = support_title
=======
            support_loc.title = support_title
>>>>>>> a943d23 (LaTeX macro ready, times out when saving due to pdf generation)
            support_loc.content_latex = support_content
            support_loc.creator = (request.user,)
>>>>>>> a84a86d (Fixing Request Authentication)
            support_loc.save()

            for attachment in support_attachments:
                blob = Blob(
                    file=attachment,
                    content_type=attachment.content_type,
                    filename=attachment.name,
                )
                blob.save()

                support_attachment_instance = Support_Attachment(
                    support=support_loc,
                    lang_code=support_loc.lang_code,
                    dialect_code=support_loc.dialect_code,
                    filename=blob.filename,
                    blob_key=blob,
                )
                support_attachment_instance.save()

            return redirect(f"/edit_quiz_add_support/{quiz_id}")

        return render(
            request,
            "mentapp/edit_support.html",
            {
                "quiz_id": quiz_id,
                "form": form,
                "volumes": volumes,
                "volume_id": volume_id,
                "support_content": support_content,
                "support_id": support_id,
            },
        )

    return render(
        request,
        "mentapp/edit_support.html",
        {
            "quiz_id": quiz_id,
            "form": form,
            "volumes": volumes,
            "support_id": support_id,
        },
    )
<<<<<<< HEAD
>>>>>>> b409248 (create new support + redirect to edit_support)
    
=======

>>>>>>> 66ff12b (fully functional)

def create_question(request):
    if request.method == "POST":
        volume_id = 1
        chapters = Chapter.objects.filter(volume__volume_id=volume_id).distinct()

        question = Question.objects.create(chapter=chapters[0])
        question_loc = Question_Loc.objects.create(question=question)

        return redirect(f"/edit_question/{question.question_id}")

    return render(request, "mentapp/main.html")


def latex_window_question(request, question_id, part, width):
    return render(
        request,
        "mentapp/latex_window.html",
        {"type": "question", "part": part, "question_id": question_id, "width": width},
    )


def grab_attachments_question(question_id):
    question = get_object_or_404(Question, question_id=question_id)
    question_loc = get_object_or_404(
        Question_Loc, question=question, lang_code="ENG", dialect_code="US"
    )
    attachments = Question_Attachment.objects.filter(question=question_loc)
    attachmentsList = list()

    for attachment in attachments:
        attachmentDict = dict()
        attachmentDict["filename"] = attachment.filename
        attachmentDict["url"] = attachment.blob_key.file.url
        attachmentsList.append(attachmentDict)

    return attachmentsList


# Returns a JSON response with only the attachment files and names
def fetch_attachments_question(request, question_id):
    attachmentsList = grab_attachments_question(question_id)
    return JsonResponse({"attachments": attachmentsList})


# Returns a JSON response with the attachment files and names and the LaTeX
def fetch_attachments_inputs_question(request, question_id, part):
    question = get_object_or_404(Question, question_id=question_id)
    question_loc = get_object_or_404(
        Question_Loc, question=question, lang_code="ENG", dialect_code="US"
    )
    attachmentsList = grab_attachments_question(question_id)
    if part == "question":
        input = question_loc.question_latex
    elif part == "answer":
        input = question_loc.answer_latex
    elif part == "rubric":
        input = question_loc.rubric_latex

    return JsonResponse({"attachments": attachmentsList, "input": input})


def edit_question(request, question_id):
    question_object = get_object_or_404(Question, question_id=question_id)
    volumes = (
        Volume.objects.values_list("volume_id", flat=True)
        .distinct()
        .order_by("volume_id")
    )
    question_loc = get_object_or_404(Question_Loc, question=question_object)

    question = question_loc.question_latex
    answer = question_loc.answer_latex
    grading = question_loc.rubric_latex
    volume_id = question_object.chapter.volume.volume_id

    form = LatexForm(
        initial={
            "latex_question": question,
            "latex_answer": answer,
            "latex_grading": grading,
            "difficulty": question_object.conceptual_difficulty,
            "volume": volume_id,
            "chapter": question_object.chapter_id if question_object else None,
            "time_required": question_object.time_required_mins,
            "points": question_object.point_value,
            "pages_required": question_object.pages_required,
        }
    )

    chapters = Chapter.objects.filter(volume__volume_id=volume_id).distinct()

    chapter_locs = Chapter_Loc.objects.filter(
        chapter__chapter_id__in=chapters
    ).distinct()

    chapter_object = chapter_locs[0]

    if request.method == "POST":

        # TODO: question_object.creator = CURRENT USER

        if request.POST.get("command") == "deleteAttachment":
            attachment = get_object_or_404(
                Question_Attachment,
                question=question_loc,
                filename=request.POST.get("filename"),
            )
            attachment.blob_key.delete()
            attachment.delete()
            return JsonResponse({"success": True})
        if request.POST.get("command") == "answer":
            question_loc.answer_latex = request.POST.get("input")
            question_loc.save()
            return JsonResponse({"success": True})

        if request.POST.get("command") == "rubric":
            question_loc.rubric_latex = request.POST.get("input")
            question_loc.save()
            return JsonResponse({"success": True})

        if request.POST.get("command") == "question":
            question_loc.question_latex = request.POST.get("input")
            question_loc.save()
            return JsonResponse({"success": True})

        if request.POST.get("command") == "upload":
            for filename, file in request.FILES.items():
                name = filename
                blob = Blob(file=file, content_type=file.content_type, filename=name)
                attachment = Question_Attachment(
                    question=question_loc, blob_key=blob, filename=name
                )
                blob.save()
                attachment.save()

            return JsonResponse({"success": True, "url": blob.file.url, "name": name})

        if "submit-question" in request.POST:

            chapter_object = request.POST.get("chapter")
            chapter_string = chapter_object.split("_")
            chapter_title = chapter_string[0]
            chapter_loc = get_object_or_404(Chapter_Loc, title=chapter_title)
            question_object.chapter = chapter_loc.chapter

            question_object.conceptual_difficulty = request.POST.get("difficulty")
            question_object.time_required_mins = request.POST.get("time_required")
            question_object.point_value = request.POST.get("points")
            question_object.pages_required = request.POST.get("pages_required")
            question_object.save()

            question_loc.question_latex = question
            question_loc.answer_latex = answer
            question_loc.rubric_latex = grading
            # TODO: question_loc.creator = CURRENT USER

            question_loc.save()

            chapter_id = chapter_loc.chapter.chapter_id

            return redirect(f"/main/{volume_id}/{chapter_id}")

    if "volume-button" not in request.POST:
        chapter_object = request.POST.get("chapter")
    else:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        form = LatexForm(initial={
            'latex_question': question.latex_question,
            'latex_answer': question.latex_answer,
            'latex_grading': question.latex_grading,
            'time_required': question.time_required_mins,
            'volume': question.volume_id,
            'chapter': question.chapter.title,  # Assuming chapter has a title attribute
            'difficulty': question.conceptual_difficulty,
            'points': question.point_value,
            'pages_required': question.pages_required,
            'title': question.title,
        })

    return render(
        request,
        "mentapp/latex_question.html",
        {
            "form": form,
            "question": question,
            "volumes": volumes,
        },
    )
>>>>>>> 472b9a9 (edit buttons redirect)
=======
        return render(
            request,
            "mentapp/edit_question.html",
            {
                "form": form,
                "question_id": question_id,
                "question": question,
                "answer": answer,
                "grading": grading,
                "question_loc": question_loc,
                "volumes": volumes,
                "volume_id": volume_id,
                "chapters": chapter_locs,
                "chapter": chapter_object,
            },
<<<<<<< HEAD
    )
>>>>>>> 03d532c (page render with question info, latex not saving to db)
=======
        )
<<<<<<< HEAD
>>>>>>> a84a86d (Fixing Request Authentication)
=======
        chapter_object = chapters[0]
=======
        chapter_object = chapters[0]

    return render(
        request,
        "mentapp/edit_question.html",
        {
            "form": form,
            "question_id": question_id,
            "question": question,
            "answer": answer,
            "grading": grading,
            "volume_id": volume_id,
            "volumes": volumes,
            "chapters": chapter_locs,
            "chapter": chapter_object,
        },
    )
>>>>>>> f6e1e0c (fixing weird merge conflix)

<<<<<<< HEAD
    return render(
        request,
        "mentapp/edit_question.html",
        {
            "form": form,
            "question_id": question_id,
            "question": question,
            "answer": answer,
            "grading": grading,
            "volume_id": volume_id,
            "volumes": volumes,
            "chapters": chapter_locs,
            "chapter": chapter_object,
        },
    )
>>>>>>> a943d23 (LaTeX macro ready, times out when saving due to pdf generation)
=======

def handles(request):
    if request.method == "POST":
        if request.POST.get("platform") == "twitter":
            sitechoice = Site.objects.get(site_id=1)
        elif request.POST.get("platform") == "instagram":
            sitechoice = Site.objects.get(site_id=2)
        elif request.POST.get("platform") == "linkedin":
            sitechoice = Site.objects.get(site_id=3)
        elif request.POST.get("platform") == "facebook":
            sitechoice = Site.objects.get(site_id=4)
        elif request.POST.get("platform") == "github":
            sitechoice = Site.objects.get(site_id=5)
        elif request.POST.get("platform") == "youtube":
            sitechoice = Site.objects.get(site_id=6)
        new_handle = Handle(
            site=sitechoice,
            handle=request.POST.get("username"),
            user=request.user,
        )
<<<<<<< HEAD
        new_handle.save()
=======
        return render(request, "mentapp/login.html")
    new_handle.save()
>>>>>>> b2672c3 (Login now required to access profile)
    user_handles = Handle.objects.filter(user=request.user)
    context = {"user_handles": user_handles}
    return render(request, "mentapp/handles.html", context)


def delete_handle(request, handle, site_id, user_id):
    curr_user = get_object_or_404(User, user_id=user_id)
    curr_site = get_object_or_404(Site, site_id=site_id)
    handle = get_object_or_404(Handle, handle=handle, site=curr_site, user=curr_user)
    if request.method == "POST":
        handle.delete()
    # Redirect to the referring page, or a default page if no referrer is found
    return redirect(request.META.get("HTTP_REFERER", "/"))
<<<<<<< HEAD
>>>>>>> f4d4c28 (Fix Editing Primary Email)
=======
=======

>>>>>>> b2672c3 (Login now required to access profile)
def customLogout(request):
    if request.method == "GET":
        logout(request)
    return render(request, "mentapp/login.html")
<<<<<<< HEAD
>>>>>>> a9ea21b (Working Logout Button, picture for logout button might be nice)
=======
>>>>>>> 7b7ea34 (Fixed merge error)
