from django.views.generic import TemplateView, ListView, DetailView

from authorsExcursions.models import User, Tour
from django.db.models import Q

class HomePageView(TemplateView):
    template_name = 'home.html'

class UsersListView(ListView):
    template_name = 'users.html'
    model = User
    context_object_name = 'list_of_all_users'

class TourListView(ListView):
    template_name = 'tours.html'
    model = Tour
    context_object_name = 'list_of_all_tours'

class TourDetailView(DetailView):
    template_name = 'tour_detail.html'
    model = Tour
    context_object_name = 'tour'

# Lab 11
class SearchView(ListView):
    template_name = 'search.html'
    model = Tour
    context_object_name = 'list_of_all_tours'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Tour.objects.filter(
            Q(excCity__icontains=query) 
        ).order_by('excDate').reverse()
