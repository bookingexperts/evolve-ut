from datetime import datetime, timedelta


def check_swap_possibility(from_rentable, to_rentable, from_booking, to_booking):
    # Same booking
    if from_booking == to_booking:
        return False
    # Clear schedule
    from_rentable.old_schedule = from_rentable.schedule.copy()
    to_rentable.old_schedule = to_rentable.schedule.copy()

    for date in daterange(from_booking.start_date, from_booking.end_date):
        del from_rentable.schedule[date]
    for date in daterange(to_booking.start_date, to_booking.end_date):
        del to_rentable.schedule[date]

    # Swap possible?
    # Swap possible, return true
    if to_rentable.check_compatibility(from_booking) and from_rentable.check_compatibility(to_booking):
        return True
    else:
        from_rentable.schedule = from_rentable.old_schedule
        to_rentable.schedule = to_rentable.old_schedule
        return False


def check_extended_swap_possibility(from_rentable, from_booking, all_rentables, all_bookings):
    swap_possibilities = []
    unchecked_bookings = all_bookings.copy()

    for to_rentable in all_rentables:
        if from_rentable == to_rentable:
            continue

        from_rentable.old_schedule = from_rentable.schedule.copy()
        to_rentable.old_schedule = to_rentable.schedule.copy()

        for date in daterange(from_booking.start_date, from_booking.end_date):
            conflict_bookings = set(
                [to_rentable.schedule[date] for date in daterange(from_booking.start_date, from_booking.end_date)])

    for to_booking in all_bookings:
        schedules = []

        for rentable in all_rentables:
            schedules.extend(
                [rentable.schedule[date] for date in daterange(from_booking.start_date, from_booking.end_date)])
        to_bookings = set([booking for booking in schedules])
        swap_possibilities = list(to_bookings)

    for swap_to in swap_possibilities:
        # check if swap_to is the same booking
        if from_booking == swap_to:
            continue

        to_rentable = swap_to.rentable

        # Clear schedule of both accommodations during the booking
        from_rentable.old_schedule = from_rentable.schedule.copy()
        to_rentable.old_schedule = to_rentable.schedule.copy()

        for date in daterange(from_booking.start_date, from_booking.end_date):
            del from_rentable.schedule[date]
        for date in daterange(to_booking.start_date, to_booking.end_date):
            del to_rentable.schedule[date]

        if check_extended_swap_possibility(to_rentable, swap_to, all_rentables,
                                           unchecked_bookings.remove(from_booking)):
            return
        # Swap possible?
        # Swap possible, return true
        if to_rentable.check_compatibility(from_booking) and from_rentable.check_compatibility(to_booking):
            return True
        else:
            from_rentable.schedule = from_rentable.old_schedule
            to_rentable.schedule = to_rentable.old_schedule
            return False
    return True


# Get all rentables that have an ability to be swapped, even with conflict.
def extended_get_conflicts(from_rentable, all_rentables, from_booking):
    conflicts = {}
    for rentable in all_rentables:
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


def extended_swap_bookings_in_schedule(from_rentable, to_rentable, from_booking, to_booking):
    to_rentable.fill_planning(from_booking)
    from_rentable.fill_planning(to_booking)


def swap_bookings_in_schedule(from_rentable, to_rentable, from_booking, to_booking):
    to_rentable.fill_planning(from_booking)
    from_rentable.fill_planning(to_booking)


def swap_ships_in_schedule(from_berth, to_berth, from_vessel, to_vessel):
    # Back up the old values
    to_vessel.old_time_accepted = to_vessel.time_accepted
    from_vessel.old_time_accepted = from_vessel.time_accepted

    # Fill the new schedules

    # Schedule the ship in the other berth schedule as soon as that is possible
    scheduling_hour = from_vessel.start_time
    while scheduling_hour < to_berth.closing_time - from_vessel.handling_time[to_berth.id] and \
            not to_berth.check_compatibility(scheduling_hour, from_vessel):
        scheduling_hour += 1
    to_berth.fill_schedule(from_vessel.id, from_vessel.handling_time[to_berth.id], scheduling_hour)
    from_vessel.acceptance_time(scheduling_hour, to_berth)
    from_vessel.time_left = from_vessel.time_accepted + from_vessel.handling_time[to_berth.id]

    # Schedule the ship in the now empty slot as soon as that is possible
    scheduling_hour = to_vessel.start_time
    while scheduling_hour < from_berth.closing_time - to_vessel.handling_time[from_berth.id] and \
            not from_berth.check_compatibility(scheduling_hour, to_vessel):
        scheduling_hour += 1
    from_berth.fill_schedule(to_vessel.id, to_vessel.handling_time[from_berth.id], scheduling_hour)
    to_vessel.acceptance_time(scheduling_hour, from_berth)
    to_vessel.time_left = to_vessel.time_accepted + to_vessel.handling_time[from_berth.id]


def daterange(start_date: datetime, end_date: datetime):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
