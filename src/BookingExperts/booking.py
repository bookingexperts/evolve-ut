import sys
import requests
from datetime import datetime

_api_key = None
_admin_id = None
headers = None
date_format = '%Y-%m-%d'


class Booking:
    def __init__(self, reservation_id, start_date, end_date, rentable_type, channel_id, booking_id, rentable=None, fixed=False):
        self.id = reservation_id
        self.start_date = start_date
        self.end_date = end_date
        self.length = end_date - start_date
        self.rentable_type = rentable_type
        self.rentable = rentable
        self.fixed = fixed
        self.channel_id = channel_id
        self.booking_id = booking_id

    def stay_start(self, current_day, rentable):
        self.rentable = rentable

    def lock_rentable(self, fixed):
        self.fixed = fixed

    def check_end(self, current_day):
        if current_day == self.start_date + self.length:
            return True
        else:
            return False

    def update_rentable(self):
        data = {
            "data": {
                "id": self.booking_id,
                "type": "reservation",
                "relationships": {
                    "rentable_identity": {
                        "data": {
                            "id": self.rentable.id,
                            "type": "rentable_identity"
                        }
                    }
                }
            }
        }

        address = f'https://api.bookingexperts.nl/v3/channels/{self.channel_id}/reservations/{self.id}'
        request = requests.patch(address, headers=headers, json=data)

        if request.status_code != 200:
            raise AttributeError(request.json()['errors'][0]['detail'])

    def __str__(self):
        return f'{{id: {self.id}, start_date: {self.start_date}, end_date: {self.end_date}, length: {self.length}, ' \
               f'rentable_type: {self.rentable_type}, rentable: {self.rentable}, fixed: {self.fixed}}}'

    def __repr__(self) -> str:
        return str(self)


def get_bookings() -> [Booking]:
    params = {'include': 'reservations'}
    address = f'https://api.bookingexperts.nl/v3/administrations/{_admin_id}/bookings'
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
                rentable_id = None

                if fixed:
                    rentable_id = reservation_data['relationships']['rentable_identity']['data']['id']

                booking = Booking(reservation_id, start_date, end_date, rentable_type, channel_id, booking_id, rentable_id, fixed)

                bookings.append(booking)
                # print(booking)

        if links['next'] is None:
            break

        request = requests.get(links['next'], headers=headers)
    return bookings


def filter_on_type(rentable_type, bookings=None) -> [Booking]:
    if bookings is None:
        bookings = get_bookings()

    return [booking for booking in bookings if booking.rentable_type == rentable_type]


def initialize():
    global _api_key, _admin_id, headers
    _api_key = sys.argv[1]  # the api-key should be passed as a program argument
    _admin_id = sys.argv[2]  # the administration id should be passed as a program argument
    headers = {'Accept': 'application/vnd.api+json', 'x-api-key': _api_key}


initialize()

if __name__ == '__main__':
    bookings = get_bookings()
    print(len(bookings))
