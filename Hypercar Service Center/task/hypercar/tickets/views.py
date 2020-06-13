from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import *


class WelcomeView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', context={'services': services,
                                                             "next_ticket_number": Queue.next_ticket_number})


class TicketView(View):
    """Create order view. Returns ticket number and expected time to wait"""

    def get(self, request, *args, **kwargs):
        ticket_type = kwargs['ticket_type']

        return render(request, 'tickets/order.html',
                      context={
                          "minutes_to_wait": Queue.calculate_wait_time(ticket_type),
                          "ticket_number": Queue.get_ticket_number(ticket_type),
                      })


class OperatorView(View):
    """Operator menu. Shows the queue length for each service"""

    def get(self, request, *args, **kwargs):
        change_oil_queue = len(Queue.line_of_cars["change_oil"])
        inflate_tires = len(Queue.line_of_cars["inflate_tires"])
        diagnostic = len(Queue.line_of_cars["diagnostic"])

        return render(request, 'tickets/processing.html',
                      context={
                          "change_oil_queue": change_oil_queue,
                          "inflate_tires": inflate_tires,
                          "diagnostic": diagnostic
                      })

    def post(self, request, *args, **kwargs):
        Queue.set_next_ticket_number()
        return redirect('/processing')


class NextView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next.html',
                      context={
                          "next_ticket_number": Queue.next_ticket_number
                      })
