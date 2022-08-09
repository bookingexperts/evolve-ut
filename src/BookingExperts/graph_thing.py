from datetime import datetime, timedelta

import data.server_communication as comm
from data.booking import Booking
from src.BookingExperts.evaluation_booking import visualize

allowed_gaps = 0


def get_bookings_in_date_range(bookings, start_date, end_date):
    return [booking for booking in bookings if booking.start_date >= start_date and booking.end_date <= end_date]


def get_longest_booking_sequence(bookings: [Booking]):
    bookings = sorted(bookings, key=lambda entry: entry.start_date)

    lengths = [booking.length for booking in bookings]
    indices = [-1] * len(bookings)

    for i in range(len(bookings)):
        sublengths = [timedelta()] * i
        for k in range(i):
            if bookings[k].end_date - bookings[i].start_date <= timedelta(days=allowed_gaps):
                sublengths[k] = lengths[k]
            maximum = max(sublengths)
            lengths[i] = lengths[i] + maximum
            if maximum > timedelta():
                indices[i] = sublengths.index(maximum)

    maximum = max(lengths)
    index = lengths.index(maximum)

    result = []
    while index >= 0:
        result.append(bookings[index])
        index = indices[index]

    result.reverse()
    return result


def count_gaps(bookings: [Booking], start_date, end_date):
    result = 0
    if bookings[0].start_date - start_date > timedelta():
        result += 1

    if end_date - bookings[-1].end_date > timedelta():
        result += 1

    for i in range(1, len(bookings)):
        if bookings[i].start_date - bookings[i - 1].end_date > timedelta():
            result += 1

    return result


def main():
    global allowed_gaps
    # allowed_gaps = 0
    today = datetime(year=2022, month=5, day=17)
    print(today)
    rentable_types = comm.get_rentable_types()

    bookings = comm.filter_bookings_on_type(rentable_types[1])
    rentables = comm.filter_rentables_on_type(rentable_types[1])[:5]

    unallocated_bookings = [booking for booking in bookings if not booking.fixed]

    last_end_date = unallocated_bookings[0].end_date

    for i in range(1, len(unallocated_bookings)):
        if unallocated_bookings[i].end_date > last_end_date:
            last_end_date = unallocated_bookings[i].end_date

    while len(unallocated_bookings) > 0:
        for rentable in rentables:
            for start_date, end_date in rentable.get_free_date_ranges(today, last_end_date):
                bookings_in_range = get_bookings_in_date_range(unallocated_bookings, start_date, end_date)
                print(start_date, end_date, bookings_in_range, unallocated_bookings)

                if len(bookings_in_range) == 0:
                    continue

                possible_bookings = get_longest_booking_sequence(bookings_in_range)
                gaps = count_gaps(possible_bookings, start_date, end_date)

                if gaps <= allowed_gaps:
                    for booking in possible_bookings:
                        booking.rentable = rentable
                        rentable.fill_planning(booking)
                        unallocated_bookings.remove(booking)

        allowed_gaps += 1
        # print(allowed_gaps)
        if allowed_gaps >= (last_end_date - today).days:
            visualize(bookings)
            raise Exception('Could not calculate best solution')

    visualize(bookings)


if __name__ == '__main__':
    main()
