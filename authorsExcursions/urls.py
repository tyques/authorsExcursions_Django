from django.urls import path

from authorsExcursions.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]