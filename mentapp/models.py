from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from datetime import datetime
import uuid


def generate_user_id():
    return str(uuid.uuid4())


class User(models.Model):
    user_id = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=generate_user_id()
    )
    full_name = models.CharField(max_length=50, default="new_user")
    password_hash = models.CharField(max_length=128, default="default_password")
    org_name = models.CharField(max_length=50, default="org")
    country_code = models.CharField(max_length=10, default="code")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    primary_lang_code = models.CharField(max_length=20, default="EN")
    primary_dialect_code = models.CharField(max_length=20, default="US")

    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_quizmaker = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if not self.pk and not self.password.startswith(
    #         ("pbkdf2_sha256$", "bcrypt", "argon2")
    #     ):
    #         self.password = make_password(self.password or "password")

    #     super().save(*args, **kwargs)

    # @receiver(pre_save, sender=User)
    # def hash_password(sender, instance, **kwargs):
    # Check if the password has changed
    #    if instance._state.adding or instance.password != User.objects.get(pk=instance.pk).password:
    #       instance.password = make_password(instance.password)

    def set_password(self, raw_password):
        return make_password(password=raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password'])

    #     if commit:
    #         user.save()

    #     return user

    def __str__(self):
        return f"""{self.full_name},
            Org: {self.org_name}, Country: {self.country_code},
            Lat: {self.latitude}, Long: {self.longitude}"""


class Volume(models.Model):
    volume_id = models.AutoField(default=0, primary_key=True)


class Chapter(models.Model):
    chapter_id = models.CharField(max_length=50, primary_key=True)
    volume = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True)
    ordering = models.IntegerField(default=0)

    def __lt__(self, other):
        return self.ordering < other.ordering


class Chapter_Loc(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    title = models.CharField(max_length=200, null=True)

    class Meta:
        unique_together = ("chapter", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["chapter", "lang_code", "dialect_code"],
                name="chapter_loc_comp_pkey",
            )
        ]

    def __str__(self):
        return self.title + "_" + self.lang_code + "_" + self.dialect_code


class Question(models.Model):
    question_id = models.AutoField(default=0, primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    conceptual_difficulty = models.FloatField(default=0)
    time_required_mins = models.FloatField(default=0)
    point_value = models.FloatField(default=0)
    pages_required = models.FloatField(default=0)


class Question_Loc(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    question_latex = models.TextField()
    answer_latex = models.TextField()
    rubric_latex = models.TextField()
    date_created = models.DateField(default=now)
    date_approved = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_chapter_loc",
    )
    approver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="approved_chapter_loc",
    )

    class Meta:
        unique_together = ("question", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["question", "lang_code", "dialect_code"],
                name="question_loc_comp_pkey",
            )
        ]

    def __str__(self):
        return self.question.__str__() + "_" + self.lang_code + "_" + self.dialect_code


class Blob(models.Model):
    blob_key = models.BinaryField(primary_key=True, default=b"")
    binary_data = models.BinaryField()


class Question_Attachment(models.Model):
    question = models.ForeignKey(Question_Loc, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    filename = models.FileField(
        upload_to="question_attachments/",
    )
    blob_key = models.ForeignKey(Blob, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ("question", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["question", "lang_code", "dialect_code"],
                name="question_attachment_comp_pkey",
            )
        ]


class Support_Attachment(models.Model):
    question = models.ForeignKey(Question_Loc, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
    filename = models.FileField(
        upload_to="support_attachments/",
    )
    blob_key = models.ForeignKey(Blob, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ("question", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["question", "lang_code", "dialect_code"],
                name="support_attachment_comp_pkey",
            )
        ]


class Quiz(models.Model):
    quiz_id = models.AutoField(default=0, primary_key=True)
    conceptual_difficulty = models.FloatField()
    time_required_mins = models.IntegerField()
    calculator_allowed = models.BooleanField(default=False)
    computer_allowed = models.BooleanField(default=False)
    internet_allowed = models.BooleanField(default=False)
    book_allowed = models.BooleanField(default=False)
    volume = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)


class Quiz_Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=0)

    class Meta:
        unique_together = ("quiz", "question")
        indexes = [
            models.Index(fields=["quiz", "question"], name="quiz_question_comp_pkey")
        ]

    def __lt__(self, other):
        return self.ordering < other.ordering


class Quiz_Rendering(models.Model):
    rendering_id = models.AutoField(default=0, primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    lang_code = models.CharField(default="EN", max_length=5)
    dialect_code = models.CharField(default="US", max_length=5)
    date_created = models.DateField(default=now)
    paper_size = models.CharField(default="8x11", max_length=50)
    blob_key = models.ForeignKey(Blob, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ("quiz", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["quiz", "lang_code", "dialect_code"],
                name="quiz_rendering_comp_pkey",
            )
        ]


class Quiz_Feedback(models.Model):
    quiz = models.ForeignKey(Quiz_Rendering, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    date_created = models.DateField(default=now)
    date_completed = models.DateField(default=now)
    date_viewed = models.DateField(default=now)
    status = models.CharField(max_length=300, null=True)
    creator_id = models.CharField(max_length=50, null=True)
    viewer_id = models.CharField(max_length=50, null=True)
    challenge_rating = models.IntegerField(default=0)
    time_rating = models.IntegerField(default=0)
    comments_text = models.TextField(null=True)

    class Meta:
        unique_together = ("quiz", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["quiz", "lang_code", "dialect_code"],
                name="quiz_feedback_comp_pkey",
            )
        ]


class Email(models.Model):
    email_address = models.CharField(max_length=100, primary_key=True, default="email")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="emails",
        verbose_name="User",
    )
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


class Site(models.Model):
    site_id = models.CharField(max_length=100, primary_key=True, default="site")


class Handle(models.Model):
    handle_id = models.CharField(max_length=100, primary_key=True, default="handle")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    handle = models.CharField(max_length=50, default="handle")
    is_verified = models.BooleanField(default=False)


class Verification(models.Model):
    verifier = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="verifier_user"
    )
    verified = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="verified_user"
    )
    date_requested = models.DateTimeField(null=True, blank=True)
    date_granted = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("verifier", "verified")
        indexes = [
            models.Index(fields=["verifier", "verified"], name="verification_comp_pkey")
        ]


class Chapter_Feedback(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    date_created = models.DateField(default=now)
    status = models.CharField(max_length=300, null=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_chapter_feedback"
    )
    viewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="viewed_chapter_feedback"
    )
    creator_comment = models.CharField(max_length=300, null=True)
    viewer_comment = models.CharField(max_length=300, null=True)

    class Meta:
        unique_together = ("chapter", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["chapter", "lang_code", "dialect_code"],
                name="chapter_feedback_comp_pkey",
            )
        ]


class Language(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    is_primary = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["user", "lang_code", "dialect_code"], name="language_comp_pkey"
            )
        ]


class Support(models.Model):
    support_id = models.AutoField(primary_key=True, default=0, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class Support_Loc(models.Model):
    support = models.ForeignKey(Support, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    title_latex = models.CharField(max_length=100, null=True)
    content_latex = models.CharField(max_length=500, null=True)
    date_created = models.DateField(default=now)
    date_approved = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_support_loc"
    )
    approver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="approved_support_loc"
    )

    class Meta:
        unique_together = ("support", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["support", "lang_code", "dialect_code"],
                name="support_loc_comp_pkey",
            )
        ]


class Quiz_Support(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    support = models.ForeignKey(Support, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=0)
