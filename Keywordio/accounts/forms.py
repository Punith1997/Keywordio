from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if cleaned_data.get('password') and cleaned_data.get('confirm_password'):
            password = cleaned_data['password']
            confirm_password = cleaned_data['confirm_password']

            if password != confirm_password:
                raise forms.ValidationError(
                    "Password does not match"
                )
        else:
            raise forms.ValidationError("You must enter both password and confirm password")
