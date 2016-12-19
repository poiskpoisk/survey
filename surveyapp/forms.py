from django import forms
from surveyapp.models import Customer, Survey, MultipleChoicesQS


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['start_time']


class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['customer']
