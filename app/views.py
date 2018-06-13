from django.contrib import messages
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from app.forms import ImagerForm
from app.helpers import get_image, handle_uploaded_file


class MainPageView(TemplateView):
    template_name = 'app/mainpage.html'


class UploadImageFormView(FormView):
    template_name = 'app/image/form.html'
    form_class = ImagerForm
    success_url = reverse_lazy('upload-image-form')

    def form_valid(self, form):
        title = (form.cleaned_data.get('title'))
        image = get_image(title)
        if image:
            handle_uploaded_file(form.cleaned_data.get('image'),
                                 '{}.{}'.format(title, image.rsplit('.', 1)[1]))
            messages.info(self.request, '{} image changed'.format(title))
        else:
            handle_uploaded_file(form.cleaned_data.get('image'),
                                 '{}.{}'.format(title, form.cleaned_data.get('image').name.rsplit('.', 1)[1]))
            messages.info(self.request, '{} image uploaded'.format(title))
        return super(UploadImageFormView, self).form_valid(form)


class ImageView(TemplateView):
    template_name = 'app/image/detail.html'

    def get(self, request, *args, **kwargs):
        image_location = get_image(self.kwargs.get('name'))
        if image_location:
            kwargs['image_url'] = image_location
            kwargs['title'] = '{} image'.format(self.kwargs.get('name'))
            return super(ImageView, self).get(request, *args, **kwargs)
        return HttpResponseNotFound()
