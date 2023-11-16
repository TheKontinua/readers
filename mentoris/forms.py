from django import forms
from mentapp.models import User


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

        if commit:
            instance.save()
        return instance
