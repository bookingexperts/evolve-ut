import itertools


class Rentable:
    new_id = itertools.count().__next__
    id: int

    def __init__(self, opening_date, closing_date, nr_rentables, type):
        self.id = Rentable.new_id() % nr_rentables
        self.opening_date = opening_date
        self.closing_date = closing_date
        self.schedule = [""] * int(closing_date)
        for i in range(0, opening_date):
            self.schedule[i] = "XX"
        for j in range(closing_date, len(self.schedule)):
            self.schedule[j] = "XX"
        self.availability = False
        self.old_schedule = self.schedule

    def define_closing_date(self, latest_date):
        for i in range(self.closing_date, latest_date):
            self.schedule.append("XX")

    def update_availibility(self, current_day):
        if not self.schedule[current_day]:
            self.availability = True
        else:
            self.availability = False

    def check_compatibility(self, current_day, booking):
        if booking.locked_on != -1 and booking.locked_on != self.id:
            return False
        for day in range(current_day, current_day + booking.length):
            if self.schedule[day]:
                return False
        return True

    def fill_planning(self, booking_id, length, current_day):
        for hour in range(current_day, current_day + length):
            self.schedule[hour] = booking_id
            self.availability = False
