from datetime import datetime

from src.BookingExperts.data.booking import Booking
import src.BookingExperts.data.server_communication as comm


def main():
    rentable_types = comm.get_rentable_types()
    rentables = comm.filter_rentables_on_type(rentable_types[0])[:5]

    start_date = datetime(year=2022, month=6, day=1)
    end_date = datetime(year=2022, month=6, day=13)

    new_booking = Booking(-1, start_date, end_date, rentable_types[0], rentable=rentables[4])
    comm.post_booking(new_booking)


if __name__ == '__main__':
    main()
