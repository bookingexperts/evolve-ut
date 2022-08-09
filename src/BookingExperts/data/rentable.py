from datetime import datetime, timedelta

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
        self.old_schedule = self.schedule.copy()

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

    def get_agenda_periods(self):
        result = []
        for event in self.schedule.values():
            if event not in result:
                result.append(event)

        result.sort(key=lambda item: item.start_date)

        return result

    def __repr__(self) -> str:
        return f'{{id: {self.id}, opening_date: {self.opening_date}, closing_date: {self.closing_date}, ' \
               f'type: {self.type}}}'

    def get_free_date_ranges(self, start_date, end_date) -> [(datetime, datetime)]:
        result = []
        minimum = max(start_date, self.opening_date)
        occupied_dates = [period for period in self.get_agenda_periods() if period.start_date >= minimum]
        # print(occupied_dates)
        if len(occupied_dates) == 0:
            return [(start_date, end_date)]

        if minimum < occupied_dates[0].start_date:
            result.append((start_date, occupied_dates[0].start_date))

        for i in range(1, len(occupied_dates)):
            if occupied_dates[i].start_date - occupied_dates[i - 1].end_date > timedelta(days=1):
                result.append((occupied_dates[i - 1].end_date, occupied_dates[i].start_date))

        if occupied_dates[-1].end_date < end_date:
            result.append((occupied_dates[-1].end_date, end_date))

        # print(self.id, result)
        return result

    def deepcopy(self):
        copy = Rentable(self.opening_date, self.closing_date, self.id, self.type)
        copy.schedule = self.schedule.copy()
        return copy

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, Rentable):
            return self.__hash__() == other.__hash__()
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class BlockedPeriod:
    def __init__(self, start_date: datetime, end_date: datetime, rentable: Rentable):
        self.start_date = start_date
        self.end_date = end_date
        self.rentable = rentable
        self.fixed = True

    def copy(self):
        return BlockedPeriod(self.start_date, self.end_date, self.rentable)
