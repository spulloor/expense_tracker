from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import django.core.validators as validators
import re


from django import forms
from django.contrib.auth import authenticate

User = get_user_model()  # Use custom model if defined

def validate_name(value):
    if not value.isalpha() or len(value) < 3 or len(value) > 15:
        raise ValidationError('Name must be 3-15 characters (alphabets and spaces only).')

class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    password1 = forms.CharField(max_length=12, required=True, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=12, required=True, label='Confirm Password', widget=forms.PasswordInput)
    name = forms.CharField(max_length=15, required=True, validators=[
        validate_name  # Custom validator for name (defined below)
    ])
    email = forms.EmailField(required=True, validators=[
        validators.EmailValidator  # Built-in email validation
    ])

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 5 or len(username) > 20:
            raise ValidationError('Username must be 5-20 characters long.')
        if not username[0].isalpha():
            raise ValidationError('Username must start with an alphabet.')
        if re.search(r'[^\w\s]', username):
            raise ValidationError('Username cannot contain special characters.')
        return username

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if len(password) < 10 or len(password) > 12:
            raise ValidationError('Password must be 10-12 characters long.')
        # Include robust password complexity checks using libraries like zxcvbn
        # https://pypi.org/project/zxcvbn/
        return password
    
    def clean_password2(self):

        try:
            password1 = self.clean_password1()
            password2 = self.cleaned_data['password2']

            if password1 != password2:
                raise ValidationError('Your password confirmation should be same as your entered password')
        except KeyError:
            raise ValidationError('Cannot access password1..')
        
        return password2

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password1', 'password2')



class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email", max_length=150, widget=forms.TextInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')

        if not username_or_email:
            raise forms.ValidationError(("Username or email is required."), code='username_required')

        try:
            User.objects.get_by_username_or_email(username_or_email)
        except:
            raise forms.ValidationError('User does not exists')

        return username_or_email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username_or_email')

        if username:

            user = authenticate(username=username, password=password)

            if password and not user:
                raise forms.ValidationError(('Incorrect password.'), code='incorrect_password')

        else:
            raise forms.ValidationError('Password is required', code='incorrect_password')
            
        return password

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')
        user = None

        if username_or_email and password:
            user = authenticate(username=username_or_email, password=password)
        

        cleaned_data['user'] = user
        return cleaned_data
