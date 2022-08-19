from datetime import datetime, timedelta


# Get all rentables that have an ability to be swapped, even with conflict.
def extended_get_conflicts(from_rentable, all_rentables, from_booking):
    conflicts = {}
    for rentable in all_rentables.values():
        if from_rentable is not None and rentable.rentable_id == from_rentable.rentable_id:
            continue
        booking_conflicts = get_bookings_in_schedule(rentable, from_booking.start_date, from_booking.end_date)
        if booking_conflicts is not None:
            conflicts[rentable] = booking_conflicts
    return conflicts


# Get all bookings in a specific schedule period
def get_bookings_in_schedule(rentable, start_date, end_date):
    booking_conflicts = []
    for date in daterange(start_date, end_date):
        if date in rentable.schedule:
            booking = rentable.schedule[date]
            if booking.placed:
                return None
            booking_conflicts.append(rentable.schedule[date])
    return set(booking_conflicts)


def daterange(start_date: datetime, end_date: datetime):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
