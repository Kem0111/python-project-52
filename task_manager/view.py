from django.shortcuts import render
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = 'index.html'

    def get(self, request, **kwargs):
        return render(request, 'index.html')
