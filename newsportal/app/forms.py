from django import forms
from .models import News
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class NewsForm(forms.ModelForm):
    description = forms.CharField(min_length=20)    # can be defined in clean method

    class Meta:
        model = News
        # fields = '__all__'    # All fields can be specified at once
        fields = [
            'name',
            'description',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()      # call the 'clean' method of the parent class
        description = cleaned_data.get('description')
        name = cleaned_data.get('name')
        if name == description:
            raise ValidationError({"name": "Name and Description must be different!"})
        if name[0].islower():
            raise ValidationError(
                "Name must begin with Capital letter"
            )
        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

