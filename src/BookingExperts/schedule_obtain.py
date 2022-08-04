import random
from datetime import datetime, timedelta

from data.booking import Booking
from data.rentable import Rentable


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


def first_come_first_serve(bookings: [Booking], rentables: [Rentable]):
    nr_bookings = len(bookings)
    nr_rentables = len(rentables)
    booking_arrival_dates = [booking.start_date for booking in bookings]
    booking_leaving_dates = [booking.end_date for booking in bookings]
    rentable_opening_dates = [rentable.opening_date for rentable in rentables]
    rentable_closing_dates = [rentable.closing_date for rentable in rentables]

    print("Park information:\n" +
          "Number of bookings:", nr_bookings,
          "\nNumber of rentables:", nr_rentables,
          "\nArrival date of bookings:", booking_arrival_dates,
          "\nLeaving date of bookings:", booking_leaving_dates,
          "\nRentable opening date:", rentable_opening_dates,
          "\nRentable closing date:", rentable_closing_dates)

    # current_date = datetime.now()
    current_date = datetime.strptime('2022-05-16', '%Y-%m-%d')
    current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    print("current date", current_date)

    queue_for_rentables = []
    bookings_in_process = []
    handled_bookings = []
    # Create a list of all bookings and rentables
    last_closing_date = 0
    for j in rentables:
        # Loop over each timestamp to see which bookings need to be served at what time.
        if j.closing_date is not None and last_closing_date < j.closing_date:
            last_closing_date = j.closing_date
    # Loop over each timestamp to see which bookings need to be served at what date.
    while len(handled_bookings) < nr_bookings:
        current_date = current_date + timedelta(days=1)
        print(current_date)


        # Add arriving bookings to the queue
        for i in range(0, nr_bookings):
            if bookings[i].start_date == current_date:
                queue_for_rentables.append(bookings[i])

        # Set each rentables to available, if it is available
        for i in range(0, nr_rentables):
            rentables[i].update_availibility(current_date)

        # If there is a queue, loop over each booking in the queue to see if a rentable is available to handle them
        if len(queue_for_rentables) > 0:
            for booking in queue_for_rentables:
                for rentable in rentables:
                    if rentable.check_compatibility(booking) and booking.rentable is None:
                        rentable.fill_planning(booking)
                        booking.stay_start(current_date, rentable)
                        bookings_in_process.append(booking)
                        print("Booking", booking.id, "placed for day", current_date, "until",
                              current_date + booking.length)
            queue_for_rentables = [booking for booking in queue_for_rentables if booking.rentable is None]

        # Loop over all bookings that are at a rentable. If they are done, add them to the handled bookings list
        if len(bookings_in_process) > 0:
            for booking in bookings_in_process:
                if booking.check_end(current_date):
                    handled_bookings.append(booking)
            bookings_in_process = [booking for booking in bookings_in_process if current_date <= booking.end_date]
    return rentables, bookings
