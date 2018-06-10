from django.forms import forms


class ImagerForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    image = forms.ImageField()
