from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render

from .models import *


class WelcomeView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', context={'services': services})


class TicketView(View):
    """Create order view. Returns ticket number and expected time to wait"""

    line_of_cars = {
        "change_oil": [],
        "inflate_tires": [],
        "diagnostic": []
    }
    ticket_number = 0

    def get(self, request, *args, **kwargs):
        ticket_type = kwargs['ticket_type']
        minutes_to_change_oil = 2 * len(self.line_of_cars['change_oil'])
        minutes_to_inflate_tires = 5 * len(self.line_of_cars['inflate_tires'])
        minutes_to_diagnostic = 30 * len(self.line_of_cars['diagnostic'])
        minutes_to_wait = 0

        if ticket_type == 'change_oil':
            minutes_to_wait = minutes_to_change_oil
        elif ticket_type == 'inflate_tires':
            minutes_to_wait = minutes_to_inflate_tires + minutes_to_change_oil
        elif ticket_type == 'diagnostic':
            minutes_to_wait = minutes_to_diagnostic + minutes_to_inflate_tires + minutes_to_change_oil
        TicketView.ticket_number += 1
        self.line_of_cars[ticket_type].append(TicketView.ticket_number)

        return render(request, 'tickets/order.html',
                      context={
                          "ticket_number": self.ticket_number,
                          "minutes_to_wait": minutes_to_wait
                      })


class OperatorView(View):
    """Operator menu. Shows the queue length for each service"""
    def get(self, request, *args, **kwargs):
        change_oil_queue = len(TicketView.line_of_cars["change_oil"])
        inflate_tires = len(TicketView.line_of_cars["inflate_tires"])
        diagnostic = len(TicketView.line_of_cars["diagnostic"])

        return render(request, 'tickets/processing.html',
                      context={
                          "change_oil_queue": change_oil_queue,
                          "inflate_tires": inflate_tires,
                          "diagnostic": diagnostic
                      })