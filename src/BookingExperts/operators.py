def check_swap_possibility(from_rentable, to_rentable, from_booking, to_booking):
    # Same booking
    if from_booking == to_booking:
        return
    # Clear schedule
    from_rentable.old_schedule = from_rentable.schedule.copy()
    to_rentable.old_schedule = to_rentable.schedule.copy()
    for day in range(from_booking.arrival_date, from_booking.leaving_date):
        from_rentable.schedule[day] = ""
    for day in range(to_booking.arrival_date, to_booking.leaving_date):
        to_rentable.schedule[day] = ""
    # Swap possible?
    possible_to = False
    possible_from = False

    for day in range(from_booking.arrival_date, min(len(to_rentable.schedule) - from_booking.length - 1,
                                                    from_booking.leaving_date - from_booking.length)):
        if to_rentable.check_compatability(day, from_booking):
            possible_to = True

    for day in range(to_booking.arrival_date,
                     min(len(from_rentable.schedule) - to_booking.length - 1,
                        to_booking.leaving_date - to_booking.length)):
        if from_rentable.check_compatability(day, to_booking):
            possible_from = True

    # Swap possible, return true
    if possible_to and possible_from:
        return True
    else:
        from_rentable.schedule = from_rentable.old_schedule
        to_rentable.schedule = to_rentable.old_schedule
        return False

def swap_bookings_in_schedule(from_rentable, to_rentable, from_booking, to_booking):

    to_rentable.fill_schedule(from_booking.id, from_booking.length, from_booking.arrival_date)
    from_rentable.fill_schedule(to_booking.id, to_booking.length, to_booking.arrival_date)

def swap_ships_in_schedule(from_berth, to_berth, from_vessel, to_vessel):
    # Back up the old values
    to_vessel.old_time_accepted = to_vessel.time_accepted
    from_vessel.old_time_accepted = from_vessel.time_accepted

    # Fill the new schedules

    # Schedule the ship in the other berth schedule as soon as that is possible
    scheduling_hour = from_vessel.arrival_time
    while scheduling_hour < to_berth.closing_time - from_vessel.handling_time[to_berth.id] and \
            not to_berth.check_compatibility(scheduling_hour, from_vessel):
        scheduling_hour += 1
    to_berth.fill_schedule(from_vessel.id, from_vessel.handling_time[to_berth.id], scheduling_hour)
    from_vessel.acceptance_time(scheduling_hour, to_berth)
    from_vessel.time_left = from_vessel.time_accepted + from_vessel.handling_time[to_berth.id]

    # Schedule the ship in the now empty slot as soon as that is possible
    scheduling_hour = to_vessel.arrival_time
    while scheduling_hour < from_berth.closing_time - to_vessel.handling_time[from_berth.id] and \
            not from_berth.check_compatibility(scheduling_hour, to_vessel):
        scheduling_hour += 1
    from_berth.fill_schedule(to_vessel.id, to_vessel.handling_time[from_berth.id], scheduling_hour)
    to_vessel.acceptance_time(scheduling_hour, from_berth)
    to_vessel.time_left = to_vessel.time_accepted + to_vessel.handling_time[from_berth.id]
