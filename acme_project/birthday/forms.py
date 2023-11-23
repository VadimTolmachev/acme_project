from django import forms


class BirthdayForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(required=False)
    birthday = forms.DateField()
