import itertools

class Booking:
    new_id = itertools.count().__next__()
    id: str

    def __init__(self, arrival_date, leaving_date):
        self.id = f'Booking_{Booking.new_id()}'
        self.arrival_date = arrival_date
        self.leaving_date = leaving_date
        self.length = leaving_date - arrival_date
        self.start_stay = 0
        self.stay_left = 0
        self.housed_by = None

    def stay_start(self, current_day, rentable):
        self.start_stay = current_day
        self.housed_by = rentable

    # def check_stay_status(self, current_day):
    #     if current_day == self.start_stay +
