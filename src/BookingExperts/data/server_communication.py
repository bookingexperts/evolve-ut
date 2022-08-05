import sys
from datetime import datetime

import requests

from src.BookingExperts.data.booking import Booking
from src.BookingExperts.data.rentable import Rentable
from src.BookingExperts.operators import daterange

_api_key = None
_admin_id = None
headers = None
date_format = '%Y-%m-%d'
root = 'https://api.bookingexperts.nl/v3'
temporary_ids = ['92107', '92108', '92109', '92110', '92111']

def get_bookings() -> [Booking]:
    params = {'include': 'reservations', 'filter[state]': 'confirmed'}
    address = f'{root}/administrations/{_admin_id}/bookings'
    request = requests.get(address, params=params, headers=headers)

    bookings = []

    while True:
        data = request.json()['data']
        included = request.json()['included']
        links = request.json()['links']

        for booking_data in data:
            booking_id = booking_data['id']
            channel_id = booking_data['relationships']['channel']['data']['id']

            for reservation in booking_data['relationships']['reservations']['data']:
                reservation_id = reservation['id']
                reservation_data = [element for element in included if element['id'] == reservation_id][0]

                start_date = datetime.strptime(reservation_data['attributes']['start_date'], date_format)
                end_date = datetime.strptime(reservation_data['attributes']['end_date'], date_format)
                rentable_type = reservation_data['relationships']['category']['data']['id']

                fixed = reservation_data['attributes']['fixed_rentable']
                cancelled = booking_data['attributes']['state'] == 'cancelled'
                # rentable_id = None

                # if fixed:
                rentable_id = reservation_data['relationships']['rentable_identity']['data']['id']

                booking = Booking(reservation_id, start_date, end_date, rentable_type, channel_id, booking_id,
                                  rentable_id, fixed, cancelled=cancelled)

                bookings.append(booking)
                # print(booking)

        if links['next'] is None:
            break

        request = requests.get(links['next'], headers=headers)
    return bookings


def filter_bookings_on_type(rentable_type, bookings=None) -> [Booking]:
    if bookings is None:
        bookings = get_bookings()

    return [booking for booking in bookings if booking.rentable_type == rentable_type]


def update_booking_rentable(booking, rentable_id=None):
    if rentable_id is None:
        rentable_id = booking.rentable_id

    data = {
        "data": {
            "id": str(booking.id),
            "type": "reservation",
            "relationships": {
                "rentable_identity": {
                    "data": {
                        "id": str(rentable_id),
                        "type": "rentable_identity"
                    }
                }
            }
        }
    }

    address = f'{root}/channels/{booking.channel_id}/reservations/{booking.id}'
    request = requests.patch(address, headers=headers, json=data)

    if request.status_code != 200:
        raise AttributeError(request.json()['errors'][0]['detail'])


def update_multiple_booking_rentables(bookings: [Booking]):
    initial_id = bookings[0].rentable_id.id

    for booking in bookings:
        update_booking_rentable(booking, rentable_id=booking.rentable_id.id - initial_id)

    for booking in bookings:
        update_booking_rentable(booking)


def get_rentables() -> {str, Rentable}:
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

            rentable_id = rentable['relationships']['rentable_identity']['data']['id']
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


def get_rentable_types():
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


def filter_rentables_on_type(rentable_type, rentables=None):
    if rentables is None:
        rentables = get_rentables()

    return [rentable for rentable in rentables if rentable.type == rentable_type]


def main():
    bookings = get_bookings()
    rentables = get_rentables()
    print(len(bookings))


def initialize():
    global _api_key, _admin_id, headers
    _api_key = sys.argv[1]  # the api-key should be passed as a program argument
    _admin_id = sys.argv[2]  # the administration id should be passed as a program argument
    headers = {'Accept': 'application/vnd.api+json', 'x-api-key': _api_key}


initialize()

if __name__ == '__main__':
    main()
