from django import forms

class VisitorForm(forms.Form):
    handle = forms.CharField(label='Your name, merp', max_length=100)