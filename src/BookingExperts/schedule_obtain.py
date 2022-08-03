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
    nr_bookings, nr_rentables, booking_arrival_date, booking_leaving_date, rentable_opening_date, rentable_closing_date \
        = read_file(name)
    print("Park information:\n" +
          "Number of bookings:", nr_bookings,
          "\nNumber of rentables:", nr_rentables,
          "\nArrival date of bookings:", booking_arrival_date,
          "\nLeaving date of bookings:", booking_leaving_date,
          "\nRentable opening date:", rentable_opening_date,
          "\nRentable closing date:", rentable_closing_date)
    current_date = 0
    queue_for_rentables = []
    bookings_in_process = []
    handled_bookings = []
    # Create a list of all bookings and rentables
    all_bookings = [Booking(booking_arrival_date[i], booking_leaving_date[i]) for i in
                   range(0, nr_bookings)]
    all_rentables = [Rentable(rentable_opening_date[j], rentable_closing_date[j], nr_rentables) for j in range(0, nr_rentables)]
    last_closing_date = 0
    for j in all_rentables:
        if last_closing_date < j.closing_date:
            last_closing_date = j.closing_date
    for i in all_rentables:
        i.define_closing_date(last_closing_date)
    # Loop over each timestamp to see which bookings need to be served at what date.
    while len(handled_bookings) < nr_bookings:
        current_date += 1
        print(current_date)

        # Add arriving bookings to the queue
        for i in range(0, nr_bookings):
            if all_bookings[i].arrival_date == current_date:
                queue_for_rentables.append(all_bookings[i])

        # Set each rentables to available, if it is available
        for i in range(0, nr_rentables):
            all_rentables[i].update_availibility(current_date)

        # If there is a queue, loop over each booking in the queue to see if a rentable is available to handle them
        if len(queue_for_rentables) > 0:
            for booking in queue_for_rentables:
                for rentable in all_rentables:
                    if rentable.check_compatibility(current_date, booking) and booking.housed_by is None:
                        rentable.fill_planning(booking.id, booking.length, current_date)
                        booking.stay_start(current_date, rentable)
                        bookings_in_process.append(booking)
                        print("Booking", booking.id, "placed for day", current_date, "until", current_date+booking.length)
            queue_for_rentables =[booking for booking in queue_for_rentables if booking.housed_by is None]

        # Loop over all bookings that are at a rentable. If they are done, add them to the handled bookings list
        if len(bookings_in_process) > 0:
            for booking in bookings_in_process:
                if booking.check_end(current_date):
                    handled_bookings.append(booking)
            bookings_in_process = [booking for booking in bookings_in_process if current_date <= booking.leaving_date]
    return all_rentables, all_bookings
