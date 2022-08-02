import random
from booking import Booking
from rentable import Rentable
from support_methods import read_file

def generate_bookings(rooms):
    all_bookings = []
    for i in range(rooms):
        j = 0
        bookings = []
        while j < 30:
            k = j + 5

            start_date = random.randint(j, k)
            end_date = random.randint(start_date + 1, start_date + 5)
            bookings.append((start_date, end_date))

            j = end_date
        all_bookings.append(bookings)

    return all_bookings



def first_come_first_serve(name):
    nr_bookings, nr_rentables, booking_arriving_time, booking_leaving_time, rentable_opening_time, rentable_closing_time, \
        handling_time, handling_costs = read_file(name)
    current_time = 0
    queue_for_rentables = []
    bookings_in_process = []
    handled_bookings = []
    # Create a list of all bookings and rentables
    all_bookings = [Booking(booking_arriving_time[i], booking_leaving_time[i]) for i in
                   range(0, nr_bookings)]
    all_rentables = [Rentable(rentable_opening_time[j], rentable_closing_time[j], nr_rentables) for j in range(0, nr_rentables)]
    last_closing_time = 0
    for j in all_rentables:
        if last_closing_time < j.closing_date:
            last_closing_time = j.closing_date
    for i in all_rentables:
        i.define_closing_date(last_closing_time)
    # Loop over each timestamp to see which bookings need to be served at what time.
    while len(handled_bookings) < nr_bookings:
        current_time += 1

        # Add arriving bookings to the queue
        for i in range(0, nr_bookings):
            if all_bookings[i].arrival_date == current_time:
                queue_for_rentables.append(all_bookings[i])

        # Set each rentables to available, if it is available
        for i in range(0, nr_rentables):
            all_rentables[i].update_availibility(current_time)

        # If there is a queue, loop over each booking (ship) in the queue to see if a booking is available to handle them
        if len(queue_for_rentables) > 0:
            for ship in queue_for_rentables:
                for rentable in all_rentables:
                    if rentable.check_compatibility(current_time, ship):
                        rentable.fill_planning(ship.id, ship.length, current_time)
                        bookings_in_process.append(ship)
            queue_for_rentables = [booking for booking in queue_for_rentables]

        # Loop over all bookings that are at a rentable. If they are done, add them to the handled bookings list
        if len(bookings_in_process) > 0:
            for booking in bookings_in_process:
                if booking.check_active(current_time):
                    handled_bookings.append(booking)
            bookings_in_process = [booking for booking in bookings_in_process]
    return all_rentables, all_bookings
