from datetime import datetime, timedelta


def check_swap_possibility(from_rentable, to_rentable, from_booking, to_booking):
    # Same booking
    if from_booking == to_booking:
        return
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
