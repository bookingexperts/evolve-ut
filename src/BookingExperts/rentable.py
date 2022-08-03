import itertools
import sys
from datetime import datetime

from booking import Booking
import requests
from support_methods import daterange

_api_key = None
_admin_id = None
date_format = '%Y-%m-%d'


class NotAvailableError(Exception):
    pass


class Rentable:
    new_id = itertools.count.__next__
    id = int

    def __init__(self, opening_date, closing_date, rentable_id, rentable_type):
        # self.id = Rentable.new_id() % nr_rentables
        self.id = rentable_id
        self.opening_date = opening_date
        self.closing_date = closing_date
        self.type = rentable_type
        self.schedule = {}
        self.availability = False
        self.old_schedule = self.schedule.copy()

    def update_availibility(self, current_day):
        if current_day not in self.schedule.keys() or not self.schedule[current_day]:
            self.availability = True
        else:
            self.availability = False

    def check_compatibility(self, booking: Booking):
        if booking.fixed and booking.rentable != self.id:
            return False
        if booking.arrival_date < self.opening_date or booking.leaving_date > self.closing_date:
            return False
        for date in daterange(booking.arrival_date, booking.leaving_date):
            if date in self.schedule.keys() and self.schedule[date] is not None:
                return False
        return True

    def fill_planning(self, booking: Booking):
        for date in daterange(booking.arrival_date, booking.leaving_date):
            if self.check_compatibility(booking):
                self.schedule[date] = booking
                self.availability = False
            else:
                raise NotAvailableError(
                    f'This rentable is not available between {booking.arrival_date} and {booking.leaving_date}')

    def set_planning_date(self, date: datetime, reason):
        self.schedule[date] = reason

    def __repr__(self) -> str:
        return f'{{id: \'{self.id}\', opening_date: \'{self.opening_date}, closing_date: \'{self.closing_date}, ' \
               f'type: \'{self.type}}}'


def get_rentables() -> {str, Rentable}:
    headers = {'Accept': 'application/vnd.api+json', 'x-api-key': _api_key}
    address = f'https://api.bookingexperts.nl/v3/administrations/{_admin_id}/rentables'
    request = requests.get(address, headers=headers)

    rentables = {}

    while True:
        data = request.json()['data']
        links = request.json()['links']

        for rentable in data:
            start_date = datetime.strptime(rentable['attributes']['active_from'], date_format)
            end_date = rentable['attributes']['active_till']

            if end_date is not None:
                end_date = datetime.strptime(end_date, date_format)

            rentable_id = rentable['id']
            rentable_type = rentable['relationships']['category']['data']['id']

            rentable = Rentable(start_date, end_date, rentable_id, rentable_type)
            rentables[rentable_id] = rentable
            # print(rentable)

        if links['next'] is None:
            break

        request = requests.get(links['next'], headers=headers)

    set_blocked_periods(rentables)
    return rentables


def set_blocked_periods(rentables: {str, Rentable}):
    headers = {'Accept': 'application/vnd.api+json', 'x-api-key': _api_key}
    params = {'filter[type]': 'MaintenanceAgendaPeriod'}

    address = f'https://api.bookingexperts.nl/v3/administrations/{_admin_id}/agenda_periods'
    request = requests.get(address, headers=headers, params=params)

    while True:
        data = request.json()['data']
        links = request.json()['links']

        for period in data:
            rentable_id = period['relationships']['rentable']['data']['id']
            start_date = datetime.strptime(period['attributes']['start_date'], date_format)
            end_date = datetime.strptime(period['attributes']['end_date'], date_format)

            for date in daterange(start_date, end_date):
                rentables[rentable_id].set_planning_date(date, 'maintenance')

        if links['next'] is None:
            break

        request = requests.get(links['next'], headers=headers)


def initialize():
    global _api_key, _admin_id
    _api_key = sys.argv[1]  # the api-key should be passed as a program argument
    _admin_id = sys.argv[2]  # the administration id should be passed as a program argument


def filter_on_type(rentable_type, rentables=None):
    if rentables is None:
        rentables = get_rentables()

    return [rentable for rentable in rentables if rentable.type == rentable_type]


def get_rentable_types():
    headers = {'Accept': 'application/vnd.api+json', 'x-api-key': _api_key}
    address = f'https://api.bookingexperts.nl/v3/administrations/{_admin_id}/categories'
    request = requests.get(address, headers=headers)

    types = []

    while True:
        data = request.json()['data']
        links = request.json()['links']

        for rentable_type in data:
            types.append(rentable_type['id'])

        if links['next'] is None:
            break

        request = requests.get(links['next'], headers=headers)

    return types


initialize()

if __name__ == '__main__':
    get_rentables()
