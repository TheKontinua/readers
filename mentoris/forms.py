from django import forms
from mentapp.models import User, Quiz


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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    org_name = forms.CharField(required=False)
    latitude = forms.DecimalField(required=False)
    longitude = forms.DecimalField(required=False)

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Manually handle optional fields with default values
        for field in self.fields:
            form_value = self.cleaned_data.get(field)
            if form_value is None:
                default_value = User._meta.get_field(field).default
                setattr(instance, field, default_value)

        password = self.cleaned_data.get("password_hash")
        setattr(instance, "password_hash", self.Meta.model.set_password(self, password))

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
