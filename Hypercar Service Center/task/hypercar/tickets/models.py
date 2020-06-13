from django.db import models
from collections import deque

services = {
    'change_oil': 'Change oil',
    'inflate_tires': 'Inflate tires',
    'diagnostic': 'Get diagnostic test'
}


class Queue:
    ticket_number = 0
    next_ticket_number = 0

    line_of_cars = {
        "change_oil": deque(),
        "inflate_tires": deque(),
        "diagnostic": deque()
    }

    @classmethod
    def get_ticket_number(cls, ticket_type):
        cls.ticket_number += 1
        cls.line_of_cars[ticket_type].append(cls.ticket_number)
        return cls.ticket_number

    @classmethod
    def get_next_ticket_number(cls):
        return cls.next_ticket_number

    @classmethod
    def calculate_wait_time(cls, ticket_type):
        """Pre-calculates the wait time"""

        minutes_to_change_oil = 2 * len(cls.line_of_cars['change_oil'])
        minutes_to_inflate_tires = 5 * len(cls.line_of_cars['inflate_tires'])
        minutes_to_diagnostic = 30 * len(cls.line_of_cars['diagnostic'])
        minutes_to_wait = 0

        if ticket_type == 'change_oil':
            minutes_to_wait = minutes_to_change_oil
        elif ticket_type == 'inflate_tires':
            minutes_to_wait = minutes_to_inflate_tires + minutes_to_change_oil
        elif ticket_type == 'diagnostic':
            minutes_to_wait = minutes_to_diagnostic + minutes_to_inflate_tires + minutes_to_change_oil

        return minutes_to_wait

    @classmethod
    def set_next_ticket_number(cls):
        """Sets next ticket number"""

        if len(cls.line_of_cars['change_oil']) > 0:
            cls.next_ticket_number = cls.line_of_cars['change_oil'].popleft()
        elif len(cls.line_of_cars['inflate_tires']) > 0:
            cls.next_ticket_number = cls.line_of_cars['inflate_tires'].popleft()
        elif len(cls.line_of_cars['diagnostic']) > 0:
            cls.next_ticket_number = cls.line_of_cars['diagnostic'].popleft()
        else:
            cls.next_ticket_number = 0
