import sys
import requests
from datetime import datetime

_api_key = None
_admin_id = None
date_format = '%Y-%m-%d'


class Booking:
    def __init__(self, booking_id, start_date, end_date, rentable_type, rentable=None, fixed=False):
        self.id = booking_id
        self.start_date = start_date
        self.end_date = end_date
        self.length = end_date - start_date
        self.rentable_type = rentable_type
        self.rentable = rentable
        self.fixed = fixed

    def stay_start(self, current_day, rentable):
        self.rentable = rentable

    def lock_rentable(self, fixed):
        self.fixed = fixed

    def check_end(self, current_day):
        if current_day == self.start_date + self.length:
            return True
        else:
            return False

    def __str__(self):
        return f'{{id: \'{self.id}\', start_date: \'{self.start_date}\', end_date: \'{self.end_date}\', ' \
               f'length: \'{self.length}\', rentable_type: \'{self.rentable_type}\', locked_on: \'{self.rentable}\', fixed: \'{self.fixed}\'}}'

    def __repr__(self) -> str:
        return str(self)


def get_bookings() -> [Booking]:
    headers = {'Accept': 'application/vnd.api+json', 'x-api-key': _api_key}
    params = {'include': 'rentable', 'filter[type]': 'ReservationAgendaPeriod'}
    address = f'https://api.bookingexperts.nl/v3/administrations/{_admin_id}/agenda_periods'
    request = requests.get(address, params=params, headers=headers)

    bookings = []

    while True:
        data = request.json()['data']
        included = request.json()['included']
        links = request.json()['links']

        for period in data:
            start_date = datetime.strptime(period['attributes']['start_date'], date_format)
            end_date = datetime.strptime(period['attributes']['end_date'], date_format)
            rentable_id = period['relationships']['rentable']['data']['id']

            for entry in included:
                if entry['id'] == rentable_id:
                    rentable_type = entry['relationships']['category']['data']['id']
                    break

            booking = Booking(period['id'], start_date, end_date, rentable_type)
            bookings.append(booking)
            print(booking)

        if links['next'] is None:
            break

        request = requests.get(links['next'], headers=headers)
    return bookings


def filter_on_type(rentable_type, bookings=None) -> [Booking]:
    if bookings is None:
        bookings = get_bookings()

    return [booking for booking in bookings if booking.rentable_type == rentable_type]


def initialize():
    global _api_key, _admin_id
    _api_key = sys.argv[1]  # the api-key should be passed as a program argument
    _admin_id = sys.argv[2]  # the administration id should be passed as a program argument


initialize()

if __name__ == '__main__':
    get_bookings()
