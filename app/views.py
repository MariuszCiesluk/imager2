# Create your views here.
from django.views import View
from django.views.generic import FormView

from app.forms import ImagerForm


class UploadImageFormView(FormView):
    form_class = ImagerForm


class ImageView(View):
    pass