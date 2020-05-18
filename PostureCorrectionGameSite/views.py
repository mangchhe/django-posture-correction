from django.views.generic import TemplateView
from django.views.generic import CreateView 
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy

from django.contrib.auth.mixins import AccessMixin
from django.views.defaults import permission_denied


#--- Homepage
class HomeView(TemplateView):
    template_name = 'home.html'


