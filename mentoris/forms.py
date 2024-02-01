from django import forms
from mentapp.models import User


class LatexForm(forms.Form):
    latex_question = forms.CharField(widget=forms.Textarea(attrs={"class": "latex-input-field"}), required=False)
    latex_answer = forms.CharField(widget=forms.Textarea(attrs={"class": "latex-input-field"}), required = False)
    latex_grading = forms.CharField(widget=forms.Textarea(attrs={"class": "latex-input-field"}), required=False)


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
