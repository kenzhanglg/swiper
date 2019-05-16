from django import forms
from django.forms import ValidationError

from user.models import Profile


class ProfileModelForm(forms.ModelForm):
    def clean_max_distance(self):
        cleaned_data = self.clean()
        max_distance = cleaned_data['max_distance']
        min_distance = cleaned_data['min_distance']
        if min_distance > max_distance:
            raise ValidationError('min_distance > max_distance')
        return max_distance

    def clean_max_dating_age(self):
        cleaned_data = self.clean()
        max_dating_age = cleaned_data['max_dating_age']
        min_dating_age = cleaned_data['min_dating_age']
        if min_dating_age > max_dating_age:
            raise ValidationError('min_dating_age > max_dating_age')
        return max_dating_age

    class Meta:
        model = Profile
        fields = '__all__'
