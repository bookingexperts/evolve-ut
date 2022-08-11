import copy


class Booking:
    def __init__(self, reservation_id, start_date, end_date, rentable_type, booking_id, rentable=None,
                 fixed=False, cancelled=False, placed=False):
        self.res_id = int(reservation_id)
        self.start_date = start_date
        self.end_date = end_date
        self.length = end_date - start_date
        self.placed = placed
        self.rentable = rentable
        self.fixed = fixed
        self.booking_id = int(booking_id)
        self.cancelled = cancelled
        self.rentable_type = rentable_type

    def stay_start(self, rentable):
        self.rentable = rentable

    def lock_rentable(self, fixed):
        self.fixed = fixed

    def place_rentable(self, placed):
        self.placed = placed or self.fixed

    def check_end(self, current_day):
        if current_day == self.start_date + self.length:
            return True
        else:
            return False

    def __str__(self):
        return f'{{id: {self.res_id}, start_date: {self.start_date}, end_date: {self.end_date}, length: {self.length}, ' \
               f'rentable_type: {self.rentable_type}, rentable: {self.rentable.rentable_id}, fixed: {self.fixed}}}'

    def __repr__(self) -> str:
        return str(self)

    def deepcopy(self):
        new_booking = copy.deepcopy(self)
        return new_booking
