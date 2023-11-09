from django.db import models
from django.contrib.auth.models import User
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
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
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
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
    question_text = models.TextField()
    answer_text = models.TextField()
    rubric_text = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    creator_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="creator_id")
    approver_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approver_id")
    def __str__(self):
        return self.question.__str__() + "_" + self.lang_code + "_" + self.dialect_code

class Question_Attachment(models.Model):
    question = models.ForeignKey(Question_Loc, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='question_attachments/', )

class Quiz(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True)
    conceptual_difficulty = models.FloatField()
    time_required_mins = models.IntegerField()

class Quiz_Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ordering = models.IntegerField()

    def __lt__(self, other):
        return self.ordering < other.ordering
    
class Quiz_Rendering(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
    rendering = models.FileField(upload_to='quiz_renderings/')
    date_created = models.DateField(auto_now_add=True)

class Quiz_Feedback(models.Model):
    quiz = models.ForeignKey(Quiz_Rendering, on_delete=models.CASCADE)
    lang_code = models.CharField(max_length=5)
    dialect_code = models.CharField(max_length=5)
    feedback = models.TextField()

class User(models.Model):
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
