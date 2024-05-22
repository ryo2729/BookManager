from django import forms

class ISBNForm(forms.Form):
    isbn = forms.CharField(label='ISBN', max_length=20)