import src.BookingExperts.data.server_communication as comm


def main(replacements=comm.temporary_ids):
    bookings = comm.get_bookings()
    initial = bookings[0].rentable.id

    rentable_type = comm.get_rentable_types()[0]

    for booking in comm.filter_bookings_on_type(rentable_type, bookings):
        index = (booking.rentable.id - initial) % 5
        # print(index)
        comm.update_booking_rentable(booking, rentable_id=replacements[index])


if __name__ == '__main__':
    main()
