from datetime import datetime

from src.BookingExperts.data.booking import Booking
from src.BookingExperts.operators import daterange


class NotAvailableError(Exception):
    pass


class Rentable:
    id = int

    def __init__(self, opening_date, closing_date, rentable_id, rentable_type):
        # self.id = Rentable.new_id() % nr_rentables
        self.id = int(rentable_id)
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
        if (booking.fixed and booking.rentable != self.id) or \
                booking.start_date < self.opening_date or (
                self.closing_date is not None and booking.end_date >= self.closing_date):
            return False

        for date in daterange(booking.start_date, booking.end_date):
            if date in self.schedule.keys():
                return False
        return True

    def fill_planning(self, booking: Booking):
        for date in daterange(booking.start_date, booking.end_date):
            self.schedule[date] = booking

    def remove_from_planning(self, booking: Booking):
        for date in daterange(booking.start_date, booking.end_date):
            del self.schedule[date]

    def set_planning_date(self, date: datetime, reason):
        self.schedule[date] = reason

    def __repr__(self) -> str:
        return f'{{id: {self.id}, opening_date: {self.opening_date}, closing_date: {self.closing_date}, ' \
               f'type: {self.type}}}'
