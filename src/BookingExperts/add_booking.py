import time
from datetime import datetime, timedelta

from src.BookingExperts.data.booking import Booking
import src.BookingExperts.data.server_communication as comm
import steepest_descent as descent
import src.BookingExperts.evaluation_booking as evaluate
from src.BookingExperts.operators import daterange

date_format = '%d-%m-%Y'

rentable_types = comm.get_rentable_types()
# rentables = list(comm.filter_rentables_on_type(rentable_types[0]).values)[:5]
rentables = comm.filter_rentables_on_type(rentable_types[0])[:5]
bookings = comm.filter_bookings_on_type(rentable_types[0])


def check_booking(new_booking: Booking):
    for rentable in rentables:
        if rentable.check_compatibility(new_booking):
            return True, None

    for date in daterange(new_booking.start_date, new_booking.end_date):
        nr_obstacles = 0
        for rentable in rentables:
            if date in rentable.schedule:
                nr_obstacles += 1

            if nr_obstacles == len(rentables):
                return False, None

    gaps, biggest_gap = evaluate.evaluate(bookings)
    new_situation = descent.get_best_swap_descent(gaps, biggest_gap, new_booking, bookings, 0)

    if new_situation is None:
        return False, None
    else:
        return True, new_situation


def main():
    # while True:
    #     start_date = input('Enter your date of arrival (dd-mm-yyyy): ')
    #     try:
    #         start_date = datetime.strptime(start_date, date_format)
    #         break
    #     except ValueError:
    #         pass
    #
    # while True:
    #     end_date = input('Enter your date of leaving (dd-mm-yyyy): ')
    #     try:
    #         end_date = datetime.strptime(end_date, date_format)
    #         break
    #     except ValueError:
    #         pass

    # start_date = datetime(year=2022, month=6, day=3)  # possible with moving other obstacles
    # end_date = datetime(year=2022, month=6, day=12)   # takes about 3 seconds

    # start_date = datetime(year=2022, month=5, day=22) # no obstacles
    # end_date = datetime(year=2022, month=5, day=27)

    # start_date = datetime(year=2022, month=5, day=27) # not possible
    # end_date = datetime(year=2022, month=6, day=1)

    start_date = datetime(year=2022, month=6, day=17)
    end_date = datetime(year=2022, month=7, day=2)

    new_booking = Booking(0, start_date, end_date, rentable_types[0])

    start_time = time.time()
    possible, new_situation = check_booking(new_booking)
    end_time = time.time()
    print(possible)
    if new_situation is not None:
        print('New schedule')
        evaluate.visualize(new_situation)
    elif possible:
        print('Not needed to make a new schedule')

    print('Solution found in:', end_time - start_time, 's')


if __name__ == '__main__':
    main()
