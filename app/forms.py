from django import forms


class ImagerForm(forms.Form):
    title = forms.CharField(max_length=100)
    image = forms.ImageField()

