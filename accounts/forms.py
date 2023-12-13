from django import forms
from django.contrib.auth import get_user_model, authenticate
from .models import MyUser
User = get_user_model()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})