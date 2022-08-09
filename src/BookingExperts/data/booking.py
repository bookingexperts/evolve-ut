class Booking:
    def __init__(self, reservation_id, start_date, end_date, rentable_type, booking_id, rentable=None,
                 fixed=False, cancelled=False, placed=False):
        self.id = int(reservation_id)
        self.start_date = start_date
        self.end_date = end_date
        self.length = end_date - start_date
        self.rentable_type = rentable_type
        self.rentable = rentable
        self.fixed = fixed
        self.booking_id = int(booking_id)
        self.cancelled = cancelled
        self.placed = placed

    def stay_start(self, rentable):
        self.rentable = rentable

    def lock_rentable(self, fixed):
        self.fixed = fixed

    def check_end(self, current_day):
        if current_day == self.start_date + self.length:
            return True
        else:
            return False

    def __str__(self):
        return f'{{id: {self.id}, start_date: {self.start_date}, end_date: {self.end_date}, length: {self.length}, ' \
               f'rentable_type: {self.rentable_type}, rentable: {self.rentable.id}, fixed: {self.fixed}}}'

    def __repr__(self) -> str:
        return str(self)

    def copy(self):
        new_booking = Booking(self.id, self.start_date, self.end_date, self.rentable_type, self.booking_id, self.rentable,
                       self.fixed, self.cancelled)
        new_booking.rentable = self.rentable.deepcopy()
        return new_booking
