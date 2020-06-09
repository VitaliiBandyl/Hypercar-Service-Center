from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

services = {
    'change_oil': 'Change oil',
    'inflate_tires': 'Inflate tires',
    'diagnostic': 'Get diagnostic test'
}


class WelcomeView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', context={'services': services})
