from django.urls import path

from app.views import UploadImageFormView, ImageView, MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='main-page'),
    path('upload/', UploadImageFormView.as_view(), name='upload-image-form'),
    path('image/<str:name>/', ImageView.as_view(), name='image-detail'),

]