from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from .models import *

line_of_cars = {
    "change_oil": [],
    "inflate_tires": [],
    "diagnostic": []
}
ticket_number = 0
next_ticket_number = 0


class WelcomeView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', context={'services': services,
                                                             "next_ticket_number": next_ticket_number})


def set_next_ticket_number():
    global next_ticket_number
    if len(line_of_cars['change_oil']) > 0:
        next_ticket_number = line_of_cars['change_oil'].pop(0)
    elif len(line_of_cars['inflate_tires']) > 0:
        next_ticket_number = line_of_cars['inflate_tires'].pop(0)
    elif len(line_of_cars['diagnostic']) > 0:
        next_ticket_number = line_of_cars['diagnostic'].pop(0)
    else:
        next_ticket_number = 0


class TicketView(View):
    """Create order view. Returns ticket number and expected time to wait"""

    def get(self, request, *args, **kwargs):
        global ticket_number

        ticket_type = kwargs['ticket_type']

        minutes_to_change_oil = 2 * len(line_of_cars['change_oil'])
        minutes_to_inflate_tires = 5 * len(line_of_cars['inflate_tires'])
        minutes_to_diagnostic = 30 * len(line_of_cars['diagnostic'])
        minutes_to_wait = 0

        if ticket_type == 'change_oil':
            minutes_to_wait = minutes_to_change_oil
        elif ticket_type == 'inflate_tires':
            minutes_to_wait = minutes_to_inflate_tires + minutes_to_change_oil
        elif ticket_type == 'diagnostic':
            minutes_to_wait = minutes_to_diagnostic + minutes_to_inflate_tires + minutes_to_change_oil

        ticket_number += 1
        line_of_cars[ticket_type].append(ticket_number)
        return render(request, 'tickets/order.html',
                      context={
                          "ticket_number": ticket_number,
                          "minutes_to_wait": minutes_to_wait,
                      })


class OperatorView(View):
    """Operator menu. Shows the queue length for each service"""

    def get(self, request, *args, **kwargs):
        change_oil_queue = len(line_of_cars["change_oil"])
        inflate_tires = len(line_of_cars["inflate_tires"])
        diagnostic = len(line_of_cars["diagnostic"])

        return render(request, 'tickets/processing.html',
                      context={
                          "change_oil_queue": change_oil_queue,
                          "inflate_tires": inflate_tires,
                          "diagnostic": diagnostic
                      })

    def post(self, request, *args, **kwargs):
        set_next_ticket_number()
        return redirect('/processing')


class NextView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next.html',
                      context={
                          "next_ticket_number": next_ticket_number
                      })