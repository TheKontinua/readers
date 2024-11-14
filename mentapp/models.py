from django.db import models
<<<<<<< HEAD
<<<<<<< HEAD
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.contrib.auth.hashers import make_password
=======
from django.contrib.auth.hashers import make_password, check_password
>>>>>>> 50446eb (Added password hashing)
from django.dispatch import receiver
=======
>>>>>>> de7f334 (Creator fields, no questions edge case, deleted imports)
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
import uuid
<<<<<<< HEAD
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin, BaseUserManager
<<<<<<< HEAD
from django.urls import reverse
=======
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

>>>>>>> de7f334 (Creator fields, no questions edge case, deleted imports)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
import uuid
>>>>>>> 4b3c7bd (Added email to models.py)
=======
>>>>>>> e58ea8e (Linked login page to the backend)
=======
>>>>>>> b473aa5 (added tables)
=======
=======

>>>>>>> 1d1ddb5 (edit question functionality)
class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_id=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        if not user_id:
            user_id = generate_user_id()

        user = self.model(email=email, user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_id=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_verified", True)

        return self.create_user(
            email, user_id=user_id, password=password, **extra_fields
        )

<<<<<<< HEAD
        return self.create_user(email, user_id=user_id, password=password, **extra_fields)
<<<<<<< HEAD
>>>>>>> 489da96 (Changed admin page to use email plus implemented custom user model in app)
=======
>>>>>>> 1d1ddb5 (edit question functionality)
=======
>>>>>>> de7f334 (Creator fields, no questions edge case, deleted imports)

def generate_user_id():
    return str(uuid.uuid4())

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

class User(models.Model):
    user_id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
=======
=======

>>>>>>> de7f334 (Creator fields, no questions edge case, deleted imports)
class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(
        max_length=100, primary_key=True, default="email@default.com"
    )
    user_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
>>>>>>> 489da96 (Changed admin page to use email plus implemented custom user model in app)
=======
class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=100, primary_key=True, default="email@default.com")
    user_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
>>>>>>> 1d1ddb5 (edit question functionality)
    full_name = models.CharField(max_length=50, default="new_user")
    password_hash = models.CharField(max_length=128, default="password")
    org_name = models.CharField(max_length=50, default="org")
    country_code = models.CharField(max_length=10, default="code")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    promotion_requested = models.BooleanField(default=False)
    primary_lang_code = models.CharField(max_length=20, default="EN")
    primary_dialect_code = models.CharField(max_length=20, default="US")

    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_quizmaker = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
<<<<<<< HEAD

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"""{self.full_name},
            Org: {self.org_name}, Country: {self.country_code},
            Lat: {self.latitude}, Long: {self.longitude}"""


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
=======
>>>>>>> 1d1ddb5 (edit question functionality)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

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
    volume_id = models.AutoField(primary_key=True)


class Chapter(models.Model):
<<<<<<< HEAD
<<<<<<< HEAD
    volume = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True)
<<<<<<< HEAD
    ordering = models.IntegerField()
=======
    ordering = models.IntegerField(default=0)
>>>>>>> 50446eb (Added password hashing)

    def __lt__(self, other):
        return self.ordering < other.ordering


class Chapter_Loc(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default = 'ENG')
    dialect_code = models.CharField(max_length=5, default = 'US')
    title = models.TextField()
=======
    chapter_id = models.AutoField(primary_key=True)
    volume_id = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True)
=======
    chapter_id = models.CharField(max_length=50, primary_key=True)
    volume = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True)
>>>>>>> 0bea260 (added chapter, volume, chapter_loc data)
    ordering = models.IntegerField(default=0)

    def __lt__(self, other):
        return self.ordering < other.ordering
>>>>>>> fb1dd3d (all tables added)


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
    question_id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    conceptual_difficulty = models.FloatField(default=0)
    time_required_mins = models.FloatField(default=0)
    point_value = models.FloatField(default=0)
    pages_required = models.FloatField(default=0)
    approval_requested = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)


class Question_Loc(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    question_latex = models.TextField()
    answer_latex = models.TextField()
    rubric_latex = models.TextField()
    date_created = models.DateTimeField(default=now)
    date_approved = models.DateTimeField(null=True, blank=True)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    creator_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="creator_id"
    )
    approver_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="approver_id"
    )

=======
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="creator_id")
    approver_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approver_id")
    
>>>>>>> b473aa5 (added tables)
=======
    creator_id = models.ForeignKey(
=======
    creator = models.ForeignKey(
<<<<<<< HEAD
>>>>>>> 0bea260 (added chapter, volume, chapter_loc data)
        User, on_delete=models.SET_NULL, null=True, related_name='created_chapter_loc')
=======
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_chapter_loc",
    )
>>>>>>> 50446eb (Added password hashing)
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

<<<<<<< HEAD
>>>>>>> fb1dd3d (all tables added)
=======
>>>>>>> 50446eb (Added password hashing)
    def __str__(self):
        return self.question.__str__() + "_" + self.lang_code + "_" + self.dialect_code


class Blob(models.Model):
    blob_key = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="pdfs/", null=True, blank=True)
    content_type = models.CharField(max_length=255, null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)


class Question_Attachment(models.Model):
<<<<<<< HEAD
<<<<<<< HEAD
    question = models.ForeignKey(Question_Loc, on_delete=models.CASCADE)
<<<<<<< HEAD
    attachment = models.FileField(
        upload_to="question_attachments/",
    )
=======
    question_id = models.ForeignKey(Question_Loc, on_delete=models.CASCADE)
=======
    question = models.ForeignKey(Question_Loc, on_delete=models.CASCADE)
>>>>>>> 0bea260 (added chapter, volume, chapter_loc data)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    filename = models.CharField(max_length=255)
    blob = models.ForeignKey(Blob, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ("question", "filename", "lang_code", "dialect_code")
=======
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    filename = models.CharField(max_length=255)
    blob_key = models.ForeignKey(Blob, on_delete=models.CASCADE, null=True)

    class Meta:
<<<<<<< HEAD
        unique_together = ("question","filename", "lang_code", "dialect_code")
>>>>>>> 324f15d (support view and url)
=======
        unique_together = ("question", "filename", "lang_code", "dialect_code")
>>>>>>> 0ae4eb6 (Merging Base Feedback w/ Main)
        indexes = [
            models.Index(
                fields=["question", "filename", "lang_code", "dialect_code"],
                name="question_attachment_comp_pkey",
            )
        ]


class Support(models.Model):
    support_id = models.AutoField(primary_key=True, editable=False)
    volume_id = models.ForeignKey(Volume, null=True, on_delete=models.CASCADE)
<<<<<<< HEAD
    

<<<<<<< HEAD
class Support_Attachment(models.Model):
    support = models.ForeignKey(Support, null=True, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
<<<<<<< HEAD
    filename = models.FileField(upload_to='support_attachments/', )
    blog_key = models.CharField(max_length=100)
>>>>>>> b473aa5 (added tables)
=======
    filename = models.FileField(
        upload_to="support_attachments/",
    )
    blob_key = models.ForeignKey(Blob, on_delete=models.CASCADE, null=True)
>>>>>>> fb1dd3d (all tables added)
=======
>>>>>>> 0f14dbf (view supports)
=======
>>>>>>> 0ae4eb6 (Merging Base Feedback w/ Main)


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    conceptual_difficulty = models.FloatField()
    time_required_mins = models.IntegerField()
    calculator_allowed = models.BooleanField(default=False)
    computer_allowed = models.BooleanField(default=False)
    internet_allowed = models.BooleanField(default=False)
    book_allowed = models.BooleanField(default=False)
    volume = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


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
<<<<<<< HEAD
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
<<<<<<< HEAD
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
<<<<<<< HEAD
    rendering = models.FileField(upload_to="quiz_renderings/")
    date_created = models.DateField(auto_now_add=True)
=======
    rendering = models.FileField(upload_to='quiz_renderings/')
    date_created = models.DateField(default=now)
>>>>>>> b473aa5 (added tables)

=======
=======
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
<<<<<<< HEAD
>>>>>>> 0bea260 (added chapter, volume, chapter_loc data)
    lang_code = models.CharField(default="EN",max_length=5)
    dialect_code = models.CharField(default="US",max_length=5)
=======
    lang_code = models.CharField(default="EN", max_length=5)
    dialect_code = models.CharField(default="US", max_length=5)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 50446eb (Added password hashing)
    date_created = models.DateField(default=now)
=======
    date_created = models.DateTimeField(default=now)
>>>>>>> 0e18c57 (add attachments and blobs to db)
=======
    date_created = models.DateTimeField(default=now)
>>>>>>> 324f15d (support view and url)
    paper_size = models.CharField(default="8x11", max_length=50)
    blob_key = models.ForeignKey(Blob, on_delete=models.CASCADE, null=True)

<<<<<<< HEAD
    class Meta:
        unique_together = ("quiz", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["quiz", "lang_code", "dialect_code"],
                name="quiz_rendering_comp_pkey",
            )
        ]
<<<<<<< HEAD
>>>>>>> fb1dd3d (all tables added)
=======

>>>>>>> 50446eb (Added password hashing)
=======
>>>>>>> f209290 (Multiple renderings per quiz)

class Quiz_Feedback(models.Model):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    quiz = models.ForeignKey(Quiz_Rendering, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
    feedback = models.TextField()


=======
    quiz_id = models.ForeignKey(Quiz_Rendering, on_delete=models.CASCADE)
=======
    quiz = models.ForeignKey(Quiz_Rendering, on_delete=models.CASCADE)
>>>>>>> 0bea260 (added chapter, volume, chapter_loc data)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    date_created = models.DateTimeField(default=now)
    date_completed = models.DateTimeField(default=now)
<<<<<<< HEAD
<<<<<<< HEAD
=======
    date_viewed = models.DateTimeField(default=now)
>>>>>>> 324f15d (support view and url)
=======
>>>>>>> 441d01e (supports multiple attachments)
    status = models.CharField(max_length=300, null=True)
    creator_id = models.CharField(max_length=50, null=True)
    viewer_id = models.CharField(max_length=50, null=True)
=======
    feedback_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    creator_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="creator_id"
    )
    date_created = models.DateField(default=now)
    date_completed = models.DateField(null=True, blank=True)
    viewer_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="viewer_id"
    )
>>>>>>> 0ae4eb6 (Merging Base Feedback w/ Main)
    challenge_rating = models.IntegerField(default=0)
    time_rating = models.IntegerField(default=0)
    creator_comment = models.TextField(default="")
    viewer_comment = models.TextField()

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    
>>>>>>> b473aa5 (added tables)
=======
>>>>>>> fb1dd3d (all tables added)
def generate_user_id():
    return str(uuid.uuid4())
=======

# def generate_user_id():
#     return str(uuid.uuid4())
>>>>>>> 875bd7f (models)


<<<<<<< HEAD
class User(models.Model):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    user_id = models.UUIDField(primary_key = True,  unique=True, default=generate_user_id(), editable = False)
    full_name = models.CharField(max_length=50, default='new_user')
    display_name = models.CharField(max_length=50, default='new_user')
    password = models.CharField(max_length=128, default='pwd')
    org_name = models.CharField(max_length=50, default='org')
    country_code = models.CharField(max_length=10, default='code')
=======
=======
>>>>>>> fb1dd3d (all tables added)
    user_id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    full_name = models.CharField(max_length=50, default="new_user")
<<<<<<< HEAD
<<<<<<< HEAD
    display_name = models.CharField(max_length=50, default="new_user")
    password = models.CharField(max_length=128, default="pwd")
    org_name = models.CharField(max_length=50, default="org")
    country_code = models.CharField(max_length=10, default="code")
>>>>>>> e58ea8e (Linked login page to the backend)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    primary_language = models.CharField(max_length=20, default="language")
=======
    password_hash = models.CharField(max_length=128, default="pwd")
=======
    password_hash = models.CharField(max_length=128, default="password")
>>>>>>> 0bea260 (added chapter, volume, chapter_loc data)
    org_name = models.CharField(max_length=50, default="org")
    country_code = models.CharField(max_length=10, default="code")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    primary_lang_code = models.CharField(max_length=20, default="EN")
    primary_dialect_code = models.CharField(max_length=20, default="US")
>>>>>>> fb1dd3d (all tables added)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_quizmaker = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> fb1dd3d (all tables added)
    # @receiver(pre_save, sender=User)
    # def hash_password(sender, instance, **kwargs):
    # Check if the password has changed
    #    if instance._state.adding or instance.password != User.objects.get(pk=instance.pk).password:
<<<<<<< HEAD
    #        instance.password = make_password(instance.password)

=======
    #@receiver(pre_save, sender=User)
    #def hash_password(sender, instance, **kwargs):
        # Check if the password has changed
    #    if instance._state.adding or instance.password != User.objects.get(pk=instance.pk).password:
     #       instance.password = make_password(instance.password)
    
>>>>>>> b473aa5 (added tables)
=======
    #       instance.password = make_password(instance.password)

>>>>>>> fb1dd3d (all tables added)
    def __str__(self):
        return f"""{self.full_name},
            Org: {self.org_name}, Country: {self.country_code},
            Lat: {self.latitude}, Long: {self.longitude}"""

=======
>>>>>>> 50446eb (Added password hashing)

=======
>>>>>>> c7d3d9a (Moved User model definition up the file)
class Email(models.Model):
<<<<<<< HEAD
    primary_email = models.CharField(max_length=100, primary_key=True, default="email")
=======
    email_address = models.CharField(max_length=100, primary_key=True, default="email")
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> fb1dd3d (all tables added)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
=======
    user = models.ForeignKey(User, on_delete=models.CASCADE)
>>>>>>> 0bea260 (added chapter, volume, chapter_loc data)
=======
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="emails",
        verbose_name="User",
    )
>>>>>>> 50446eb (Added password hashing)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
<<<<<<< HEAD


<<<<<<< HEAD
<<<<<<< HEAD
=======
    user_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable = False)
    password_hash = models.CharField(max_length=100)
    display_name = models.CharField(max_length=50)
    org_name = models.CharField(max_length = 100)
    country_code = models.CharField(max_length=3)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longetude = models.DecimalField(max_digits=9, decimal_places=6)
    is_verified = models.BooleanField()
    is_admin = models.BooleanField()
    is_quizmaker = models.BooleanField()
    is_active = models.BooleanField()
    
class Email(models.Model):
    email_address = models.CharField(max_length=100, primary_key = True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    is_primary = models.BooleanField()
    is_verified = models.BooleanField()
>>>>>>> 4b3c7bd (Added email to models.py)
=======
>>>>>>> e58ea8e (Linked login page to the backend)
=======
=======
class Site(models.Model):
    site_id = models.CharField(max_length=100, primary_key=True, default="site")
    name = models.CharField(max_length=100, default="name")


>>>>>>> fb1dd3d (all tables added)
class Handle(models.Model):
<<<<<<< HEAD
=======
    handle_id = models.AutoField(primary_key=True)
>>>>>>> 93564c2 (Handles saved in database, displayed on profile page)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    handle = models.CharField(max_length=50, default="handle")
    is_verified = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user', 'handle', 'site')
    def get_absolute_url(self):
        return reverse('delete_handle', args=[str(self.id)])


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
    date_created = models.DateTimeField(default=now)
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


class Support_Loc(models.Model):
    support = models.ForeignKey(Support, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default="ENG")
    dialect_code = models.CharField(max_length=5, default="US")
    title = models.CharField(max_length=100, null=True)
    content_latex = models.CharField(max_length=500, null=True)
    date_created = models.DateTimeField(default=now)
    date_approved = models.DateTimeField(default=now)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="created_support_loc",
    )
    approver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True,
        related_name="approved_support_loc"
    )

    class Meta:
        unique_together = ("support", "lang_code", "dialect_code")
        indexes = [
            models.Index(
                fields=["support", "lang_code", "dialect_code"],
                name="support_loc_comp_pkey",
            )
        ]


class Support_Attachment(models.Model):
    support = models.ForeignKey(Support_Loc, null=True, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
    filename = models.CharField(max_length=255)
    blob_key = models.ForeignKey(Blob, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ("support", "lang_code", "dialect_code", "blob_key")
        indexes = [
            models.Index(
                fields=["support", "lang_code", "dialect_code", "blob_key"],
                name="support_attachment_comp_pkey",
            )
        ]


class Quiz_Support(models.Model):
<<<<<<< HEAD
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    support_id = models.ForeignKey(Support, on_delete=models.CASCADE)
<<<<<<< HEAD
    ordering = models.IntegerField()
>>>>>>> b473aa5 (added tables)
=======
=======
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    support = models.ForeignKey(Support, on_delete=models.CASCADE)
>>>>>>> 0bea260 (added chapter, volume, chapter_loc data)
    ordering = models.IntegerField(default=0)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> fb1dd3d (all tables added)
=======
>>>>>>> 50446eb (Added password hashing)
=======

    class Meta:
        unique_together = ("quiz", "support")
        indexes = [
            models.Index(
                fields=["quiz", "support"],
                name="quiz_support_comp_pkey",
            )
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        ]
<<<<<<< HEAD
>>>>>>> 0a56ca3 (models and attachments)
=======
>>>>>>> 9ee99b0 (removed duplicate date field)
=======
        ]
>>>>>>> 1d1ddb5 (edit question functionality)
=======
        ]
>>>>>>> 7a8d51f (Fixed misc bugs related to deployment and formatting for the quiz display)
=======
        ]
>>>>>>> de7f334 (Creator fields, no questions edge case, deleted imports)
