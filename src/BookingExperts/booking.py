import itertools


class Booking:
    new_id = itertools.count().__next__
    id: str

    def __init__(self, arrival_date, leaving_date):
        self.id = f'Booking_{Booking.new_id()}'
        self.arrival_date = arrival_date
        self.leaving_date = leaving_date
        self.length = leaving_date - arrival_date
        self.housed_by = None
        self.locked_on = -1

    def stay_start(self, current_day, rentable):
        self.housed_by = rentable

    def lock_stay(self, rentable_id):
        self.locked_on = rentable_id

    def check_end(self, current_day):
        if current_day == self.arrival_date + self.length:
            return True
        else:
            return False

