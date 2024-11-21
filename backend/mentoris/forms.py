from django import forms
from mentapp.models import User, Quiz
from multiupload.fields import MultiFileField


class LatexForm(forms.Form):
    latex_question = forms.CharField(
        widget=forms.Textarea(attrs={"class": "latex-input-field"}), required=False
    )
    latex_answer = forms.CharField(
        widget=forms.Textarea(attrs={"class": "latex-input-field"}), required=False
    )
    latex_grading = forms.CharField(
        widget=forms.Textarea(attrs={"class": "latex-input-field"}), required=False
    )
    latex_support = forms.CharField(
        widget=forms.Textarea(attrs={"class": "latex-input-field"}), required=False
    )

    time_required = forms.IntegerField(initial=0)
    volume = forms.IntegerField(initial=1)
    chapter = forms.CharField(max_length=50)
    difficulty = forms.IntegerField(initial=0)
    points = forms.IntegerField(initial=0)
    pages_required = forms.DecimalField(initial=0.0)
    title = forms.CharField(max_length=50, initial="", required=True)
    attachments = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5)


class UserForm(forms.ModelForm):
    org_name = forms.CharField(required=False)
    latitude = forms.DecimalField(required=False)
    longitude = forms.DecimalField(required=False)

    class Meta:
        model = User
        fields = ['full_name', 'password_hash', 'org_name', 'country_code', 'latitude', 'longitude', 'promotion_requested', 'primary_lang_code', 'primary_dialect_code', 'is_verified', 'is_admin', 'is_quizmaker', 'is_active', 'is_staff']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Manually handle optional fields with default values
        for field in self.fields:
            if field == 'password_hash':
                instance.set_password(self.cleaned_data.get(field))
            form_value = self.cleaned_data.get(field)
            if form_value is None:
                default_value = User._meta.get_field(field).default
                setattr(instance, field, default_value)

        if commit:
            try:
                instance.save()
            except Exception as e:
                print(f"Error saving instance: {e}")
        return instance



class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"
