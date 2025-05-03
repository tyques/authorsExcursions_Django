from django.urls import path

from authorsExcursions.views import HomePageView, UsersListView, TourListView, TourDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('users', UsersListView.as_view(), name='users'),
    path('tours', TourListView.as_view(), name='tours'),
    path('tours/<int:pk>', TourDetailView.as_view(), name='tour_detail'),
]