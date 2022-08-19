"""
This file can make a backup of the current reservations and restore them.
It stores the reservation id, the rentable it was linked to, whether or not it is a fixed reservation,
the category and start- and end date.
"""

from src.BookingExperts.data.server_communication import *

date_format = '%Y-%m-%d'


def create_backup():
    bookings = get_bookings()
    with open('booking_backup.txt', 'w+') as file:
        for booking in bookings:
            start_date = booking.start_date.strftime(date_format)
            end_date = booking.end_date.strftime(date_format)

            print(booking.res_id, booking.rentable.rentable_id, booking.fixed, booking.rentable_type)
            file.write(f'{booking.res_id} {booking.rentable.rentable_id} {booking.fixed} {booking.rentable_type} '
                       f'{start_date} {end_date}\n')


def get_backup_bookings():
    bookings = []
    with open('booking_backup.txt', 'r') as file:
        for line in file:
            data = line.strip().split(' ')
            rentable = Rentable(None, None, data[1], data[3])

            booking = Booking(data[0], datetime.strptime(data[4], date_format), datetime.strptime(data[5], date_format),
                              data[3], rentable=rentable, fixed=data[2] == 'True')
            bookings.append(booking)
            print(booking)
    return bookings


def main():
    # create_backup()
    bookings = get_backup_bookings()
    rentable_types = get_rentable_types()

    for rentable_type in rentable_types:
        filtered_bookings = filter_bookings_on_type(rentable_type, bookings)
        update_multiple_booking_rentables(filtered_bookings)


if __name__ == '__main__':
    main()
