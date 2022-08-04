import src.BookingExperts.data.server_communication as comm


def main():
    bookings = comm.get_bookings()
    initial = bookings[0].rentable_id

    rentable_type = comm.get_rentable_types()[0]

    for booking in comm.filter_bookings_on_type(rentable_type, bookings):
        if booking.channel_id == 14844:
            index = (booking.rentable_id - initial) % 5
            print(index)
            comm.update_booking_rentable(booking, rentable_id=comm.temporary_ids[index])


if __name__ == '__main__':
    main()
