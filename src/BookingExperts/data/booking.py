import requests


class Booking:
    def __init__(self, reservation_id, start_date, end_date, rentable_type, channel_id, booking_id, rentable_id=None,
                 fixed=False, cancelled=False):
        self.id = int(reservation_id)
        self.start_date = start_date
        self.end_date = end_date
        self.length = end_date - start_date
        self.rentable_type = rentable_type
        self.rentable_id = int(rentable_id)
        self.fixed = fixed
        self.channel_id = int(channel_id)
        self.booking_id = int(booking_id)
        self.cancelled = cancelled

    def stay_start(self, current_day, rentable):
        self.rentable_id = rentable

    def lock_rentable(self, fixed):
        self.fixed = fixed

    def check_end(self, current_day):
        if current_day == self.start_date + self.length:
            return True
        else:
            return False

    def __str__(self):
        return f'{{id: {self.id}, start_date: {self.start_date}, end_date: {self.end_date}, length: {self.length}, ' \
               f'rentable_type: {self.rentable_type}, rentable: {self.rentable_id}, fixed: {self.fixed}, channel_id: {self.channel_id}}}'

    def __repr__(self) -> str:
        return str(self)
