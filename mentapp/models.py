from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.utils.timezone import now
from django.db.models.signals import pre_save
from datetime import datetime
import uuid


class Volume(models.Model):
    number = models.IntegerField(default=0, primary_key=True)

class Chapter(models.Model):
    volume = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True)
    ordering = models.IntegerField()
    def __lt__(self, other):
        return self.ordering < other.ordering
    
class Chapter_Loc(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default = 'ENG')
    dialect_code = models.CharField(max_length=5, default = 'US')
    title = models.TextField()

    def __str__(self):
        return self.title + "_" + self.lang_code + "_" + self.dialect_code


class Question(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    conceptual_difficulty = models.FloatField()
    time_required_mins = models.IntegerField()
    point_value = models.FloatField()


class Question_Loc(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default = 'ENG')
    dialect_code = models.CharField(max_length=5, default = 'US')
    question_text = models.TextField()
    answer_text = models.TextField()
    rubric_text = models.TextField()
    date_created = models.DateField(default=now)
    date_approved = models.DateTimeField(null=True, blank=True)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="creator_id")
    approver_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approver_id")
    
    def __str__(self):
        return self.question.__str__() + "_" + self.lang_code + "_" + self.dialect_code


class Question_Attachment(models.Model):
    question_id = models.ForeignKey(Question_Loc, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default = 'ENG')
    dialect_code = models.CharField(max_length=5, default = 'US')
    filename = models.FileField(upload_to='question_attachments/', )
    blog_key = models.CharField(max_length=100, null=True)

class Support_Attachment(models.Model):
    question_id = models.ForeignKey(Question_Loc, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
    filename = models.FileField(upload_to='support_attachments/', )
    blog_key = models.CharField(max_length=100)


class Quiz(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    conceptual_difficulty = models.FloatField()
    time_required_mins = models.IntegerField()


class Quiz_Question(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ordering = models.IntegerField()

    def __lt__(self, other):
        return self.ordering < other.ordering
    
class Quiz_Rendering(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
    rendering = models.FileField(upload_to='quiz_renderings/')
    date_created = models.DateField(default=now)

class Quiz_Feedback(models.Model):
    quiz_id = models.ForeignKey(Quiz_Rendering, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default = 'ENG')
    dialect_code = models.CharField(max_length=5, default = 'US')
    date_created = models.DateField(default=now)
    status = models.CharField(max_length=300, null=True)
    creator_id = models.CharField(max_length=50, null=True)
    viewer_id = models.CharField(max_length=50, null=True)
    creator_comment = models.CharField(max_length=300, null=True)
    viewer_comment = models.CharField(max_length=300, null=True)

    
def generate_user_id():
    return str(uuid.uuid4())

class User(models.Model):
    user_id = models.UUIDField(primary_key = True,  unique=True, default=generate_user_id(), editable = False)
    full_name = models.CharField(max_length=50, default='new_user')
    display_name = models.CharField(max_length=50, default='new_user')
    password = models.CharField(max_length=128, default='pwd')
    org_name = models.CharField(max_length=50, default='org')
    country_code = models.CharField(max_length=10, default='code')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    primary_language = models.CharField(max_length=20, default='language')
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_quizmaker = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    #@receiver(pre_save, sender=User)
    #def hash_password(sender, instance, **kwargs):
        # Check if the password has changed
    #    if instance._state.adding or instance.password != User.objects.get(pk=instance.pk).password:
     #       instance.password = make_password(instance.password)
    
    def __str__(self):
        return f"""{self.full_name},
            {self.display_name}, 
            Org: {self.org_name}, Country: {self.country_code},
            Lat: {self.latitude}, Long: {self.longitude}"""

class Email(models.Model):
    primary_email = models.CharField(max_length=100, primary_key = True, default="email")
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


class Handle(models.Model):
    handle_id = models.CharField(max_length=100, primary_key = True, default="email")
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    site = models.BooleanField(default=False)
    handle = models.CharField(max_length=50, default='handle')
    is_verified = models.BooleanField(default=False)


class Verification(models.Model):
    verifier_id = models.CharField(max_length=100, default="verifier")
    verified_id = models.CharField(max_length=100, default="verified")
    date_requested = models.DateTimeField(null=True, blank=True)
    date_granted = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('verifier_id', 'verified_id')


class Chapter_Feedback(models.Model):
    chapter_id = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default = 'ENG')
    dialect_code = models.CharField(max_length=5, default = 'US')
    date_created = models.DateField(default=now)
    status = models.CharField(max_length=300, null=True)
    creator_id = models.CharField(max_length=50, null=True)
    viewer_id = models.CharField(max_length=50, null=True)
    creator_comment = models.CharField(max_length=300, null=True)
    viewer_comment = models.CharField(max_length=300, null=True)


class Language(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default = 'ENG')
    dialect_code = models.CharField(max_length=5, default = 'US')   
    is_primary = models.BooleanField(default=True)


class Support(models.Model):
    support_id = models.CharField(Chapter, primary_key=True, default=generate_user_id(), editable = False)
    creator_id = models.CharField(max_length=50, null=True)
    chapter_id = models.CharField(max_length=50, null=True)


class Support_Loc(models.Model):
    support_id = models.ForeignKey(Support, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5, default = 'ENG')
    dialect_code = models.CharField(max_length=5, default = 'US')
    title_latex = models.CharField(max_length=100, null=True)
    content_latex = models.CharField(max_length=500, null=True)
    date_created = models.DateField(default=now)
    date_approved = models.DateTimeField(null=True, blank=True)
    creator_id = models.CharField(max_length=50, null=True)
    approver_id = models.CharField(max_length=50, null=True)
    

class Quiz_Support(models.Model):
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    support_id = models.ForeignKey(Support, on_delete=models.CASCADE)
    ordering = models.IntegerField()
