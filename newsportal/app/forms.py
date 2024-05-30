from django import forms
from .models import News
from django.core.exceptions import ValidationError


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
        # if description is not None and len(description) < 20:
        #     raise ValidationError({"description": "Description cannot be shorter than 20 symbols!"})
        name = cleaned_data.get('name')
        if name == description:
            raise ValidationError({"name": "Name and Description must be different!"})
        if name[0].islower():
            raise ValidationError(
                "Name must begin with Capital letter"
            )
        return cleaned_data
