from django.urls import path

from app.views import UploadImageFormView, ImageView

urlpatterns = [
    path('upload/', UploadImageFormView.as_view(), name='upload-image-form'),
    path('image/<str:name>/', ImageView.as_view(), name='image-detail'),
    path('image/', ImageView.as_view(), name='image-detail'),

]