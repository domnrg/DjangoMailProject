from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "phone", "avatar", "country", "password1", "password2"]


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(self.request, email=email, password=password)
            if user is None:
                raise forms.ValidationError("Неверный email или пароль.")

            if not user.is_active:
                raise forms.ValidationError("Аккаунт не подтверждён. Проверьте email.")

            self.user = user

        return self.cleaned_data

    def get_user(self):
        return self.user
