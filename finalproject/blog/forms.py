from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, Post


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(required=False)
    city = forms.CharField(required=False)
    user_phone = forms.CharField(max_length=14, required=False)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'birth_date', 'user_phone', 'city')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'body', 'image',)

