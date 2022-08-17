import sys
from datetime import datetime

import requests

from src.BookingExperts.data.booking import Booking
from src.BookingExperts.data.rentable import Rentable, BlockedPeriod
from src.BookingExperts.operators import daterange

_api_key = None
_admin_id = None
_channel_id = None
headers = None
date_format = '%Y-%m-%d'
root = 'https://api.app.ut-evolve.bookingexperts.nl/v3'
temporary_ids = ['92076', '92077', '92078', '92079', '92080']
original_ids = ['90720', '90721', '90722', '90723', '90724']
_bookings = None
_rentables = None
today = datetime(year=2022, month=5, day=16)


def get_bookings() -> [Booking]:
    global _bookings, _rentables

    if _bookings is not None:
        return _bookings

    # print(_rentables)
    if _rentables is None:
        _rentables = get_rentables()

    params = {'include': 'reservations', 'filter[state]': 'confirmed'}
    address = f'{root}/administrations/{_admin_id}/bookings'
    request = requests.get(address, params=params, headers=headers)

    _bookings = []

    while True:
        data = request.json()['data']
        included = request.json()['included']
        links = request.json()['links']

        for booking_data in data:

            for reservation in booking_data['relationships']['reservations']['data']:
                reservation_id = reservation['id']
                reservation_data = [element for element in included if element['id'] == reservation_id][0]

                start_date = datetime.strptime(reservation_data['attributes']['start_date'], date_format)
                end_date = datetime.strptime(reservation_data['attributes']['end_date'], date_format)
                rentable_type = reservation_data['relationships']['category']['data']['id']

                fixed = reservation_data['attributes']['fixed_rentable']
                cancelled = booking_data['attributes']['state'] == 'cancelled'
                cant_be_moved = fixed or (start_date <= today <= end_date)

                rentable_id = reservation_data['relationships']['rentable_identity']['data']['id']
                rentable = _rentables[rentable_id]

                booking = Booking(reservation_id, start_date, end_date, rentable_type, rentable, fixed,
                                  cancelled=cancelled, cant_be_moved=cant_be_moved)

                if fixed:
                    booking.placed = True
                rentable.fill_planning(booking)

                _bookings.append(booking)
                # print(booking)

        if links['next'] is None:
            break

        request = requests.get(links['next'], headers=headers)
    return _bookings


def filter_bookings_on_type(rentable_type, bookings=None) -> [Booking]:
    if bookings is None:
        bookings = get_bookings()

    return [booking for booking in bookings if booking.rentable_type == rentable_type]


def get_bookings_in_date_range(start_date, end_date, bookings=None):
    if bookings is None:
        bookings = get_bookings()

    return [booking for booking in bookings if booking.start_date >= start_date and booking.end_date <= end_date]


def update_booking_rentable(booking, rentable_id=None):
    if rentable_id is None:
        rentable_id = booking.rentable.rentable_id

    data = {
        "data": {
            "id": str(booking.res_id),
            "type": "reservation",
            "attributes": {
                "fixed_rentable": booking.fixed
            },
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

    address = f'{root}/administrations/{_admin_id}/reservations/{booking.res_id}'
    request = requests.patch(address, headers=headers, json=data)

    if request.status_code != 200:
        raise AttributeError(request.json()['errors'][0]['detail'])


def update_multiple_booking_rentables(bookings: [Booking]):
    initial_id = int(bookings[0].rentable.rentable_id)

    for booking in bookings:
        print('temporary placing', booking)
        index = (int(booking.rentable.rentable_id) - initial_id) % len(temporary_ids)
        update_booking_rentable(booking, rentable_id=temporary_ids[index])

    for booking in bookings:
        print('updating', booking)
        update_booking_rentable(booking)


def post_booking(booking: Booking):
    _channel_id = sys.argv[3]
    address = f'{root}/channels/{_channel_id}/reservations'
    params = {'allow_reservations_in_the_past': 'true'}

    data = {
        "data": {
            "type": "reservation",
            "attributes": {
                "start_date": booking.start_date.strftime(date_format),
                "end_date": booking.end_date.strftime(date_format),
                "guest_group": {
                    "adults": 1
                },
                "fixed_rentable": booking.fixed
            },
            "relationships": {
                "category": {
                    "data": {
                        "id": booking.rentable.type,
                        "type": "category"
                    }
                },
                "rentable_identity": {
                    "data": {
                        "id": booking.rentable.rentable_id,
                        "type": "rentable_identity"
                    }
                }
            }
        }
    }

    request = requests.post(address, headers=headers, params=params, json=data)

    if request.status_code != 201:
        raise AttributeError(request.json()['errors'][0]['detail'])


def get_rentables() -> {str, Rentable}:
    global _rentables
    if _rentables is not None:
        return _rentables

    address = f'{root}/administrations/{_admin_id}/rentables'
    request = requests.get(address, headers=headers)

    _rentables = {}

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
            _rentables[rentable_id] = rentable
            # print(rentable)

        if links['next'] is None:
            break

        request = requests.get(links['next'], headers=headers)

    set_blocked_periods(_rentables)
    return _rentables


def set_blocked_periods(rentables: {str, Rentable}):
    params = {'filter[type]': 'MaintenanceAgendaPeriod', "include": "rentable"}
    # print(rentables)

    address = f'{root}/administrations/{_admin_id}/agenda_periods'
    request = requests.get(address, headers=headers, params=params)

    while True:
        data = request.json()['data']
        included = request.json()['included']
        links = request.json()['links']

        for period in data:
            rentable_id = period['relationships']['rentable']['data']['id']
            rentable = [rentable for rentable in included if rentable['id'] == rentable_id][0]
            rentable_id = rentable['relationships']['rentable_identity']['data']['id']

            start_date = datetime.strptime(period['attributes']['start_date'], date_format)
            end_date = datetime.strptime(period['attributes']['end_date'], date_format)

            blocked_period = BlockedPeriod(start_date, end_date, rentables[rentable_id])

            for date in daterange(start_date, end_date):
                rentables[rentable_id].set_planning_date(date, blocked_period)

        if links['next'] is None:
            break

        request = requests.get(links['next'], headers=headers)


def get_rentable_types():
    address = f'{root}/administrations/{_admin_id}/categories'
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

    return [rentable for rentable in rentables.values() if rentable.type == rentable_type]


def main():
    global _rentables, _bookings
    _rentables = get_rentables()
    _bookings = get_bookings()
    # print(len(_bookings))

    # for rentable in _rentables.values():
    # print(rentable)
    # print(rentable.get_agenda_periods())


def initialize():
    global _api_key, _admin_id, _channel_id, headers
    _api_key = sys.argv[1]  # the api-key should be passed as a program argument
    _admin_id = sys.argv[2]  # the administration id should be passed as a program argument
    headers = {'Accept': 'application/vnd.api+json', 'x-api-key': _api_key}


initialize()

if __name__ == '__main__':
    main()
