import math
import time
from datetime import datetime, timedelta

from src.BookingExperts.data.booking import Booking
import src.BookingExperts.data.server_communication as comm
import steepest_descent as descent
import src.BookingExperts.evaluation_booking as evaluate
from src.BookingExperts.operators import daterange

date_format = '%d-%m-%Y'

rentable_types = comm.get_rentable_types()
rentables = comm.filter_rentables_on_type(rentable_types[0])[:5]
bookings = comm.filter_bookings_on_type(rentable_types[0])

rentable_amount = len(rentables)
recursive_depth = math.floor(math.log(500, rentable_amount - 1))
print(recursive_depth)


def check_booking(new_booking: Booking):
    for rentable in rentables:
        if rentable.check_compatibility(new_booking):
            return True, None

    if not check_date_range(new_booking.start_date, new_booking.end_date, rentables):
        return False, None

    gaps, biggest_gap = evaluate.evaluate(bookings)
    new_situation = descent.get_best_swap_descent(gaps, biggest_gap, new_booking, bookings, recursive_depth + 1)

    return new_situation is not None, new_situation


def check_fixed_booking(new_booking: Booking):
    if new_booking.rentable.check_compatibility(new_booking):
        return True, None
    else:
        for date in daterange(new_booking.start_date, new_booking.end_date):
            if date in new_booking.rentable.schedule and new_booking.rentable.schedule[date].cant_be_moved:
                print('fixed booking already exists')
                return False, None

        if not check_date_range(new_booking.start_date, new_booking.end_date, rentables):
            return False, None

        conflicts = new_booking.rentable.get_agenda_periods_in_period(new_booking.start_date, new_booking.end_date)
        new_situation = [booking for booking in bookings if booking not in conflicts]
        for conflict in conflicts:
            conflict.rentable.remove_from_planning(conflict)

        print(conflicts)
        print(new_situation)

        new_booking.rentable.fill_planning(new_booking)
        new_situation.append(new_booking)

        for conflict in conflicts:
            gaps, biggest_gap = evaluate.evaluate(new_situation)
            new_situation = descent.get_best_swap_descent(gaps, biggest_gap, conflict, new_situation,
                                                          recursive_depth + 1)
            if new_situation is None:
                break

        return new_situation is not None, new_situation


def check_date_range(start_date, end_date, rentables):
    for date in daterange(start_date, end_date):
        nr_obstacles = 0
        for rentable in rentables:
            if date in rentable.schedule and rentable.schedule[date] is not None:
                nr_obstacles += 1

            if nr_obstacles == len(rentables):
                return False
    return True


def plan_booking(new_booking, new_schedule=None):
    if new_schedule is None:
        for rentable in rentables:
            if (new_booking.start_date - timedelta(days=1) in rentable.schedule and
                rentable.schedule[new_booking.start_date - timedelta(days=1)] is not None) and \
                    (new_booking.end_date + timedelta(days=1) in rentable.schedule and
                     rentable.schedule[new_booking.end_date + timedelta(days=1)] is not None):

                for date in daterange(new_booking.start_date, new_booking.end_date):
                    if date in rentable.schedule and rentable.schedule[date] is not None:
                        break
                else:
                    new_booking.rentable = rentable
                    rentable.fill_planning(new_booking)
                    return None

        if new_schedule is None:
            gaps, biggest_gap = evaluate.evaluate(bookings)
            new_schedule = descent.get_best_swap_descent(gaps, biggest_gap, new_booking, bookings, recursive_depth + 1)

    return new_schedule


def main():
    start_date = datetime(year=2022, month=6, day=9)
    end_date = datetime(year=2022, month=6, day=18)

    new_booking = Booking(-1, start_date, end_date, rentable_types[0])

    start_time = time.time()
    possible, new_situation = check_booking(new_booking)
    end_time = time.time()
    print(possible)

    if possible:
        new_schedule = plan_booking(new_booking, new_situation)
        if new_schedule is None:
            comm.post_booking(new_booking)
        else:
            evaluate.visualize(new_schedule)

            comm.update_multiple_booking_rentables([booking for booking in new_schedule if booking.res_id != -1])
            new_booking = [booking for booking in new_schedule if booking.res_id == -1][0]

            comm.post_booking(new_booking)

    print('Solution found in:', end_time - start_time, 's')


def fixed_booking():
    start_date = datetime(year=2022, month=6, day=20)
    end_date = datetime(year=2022, month=6, day=22)
    new_booking = Booking(-1, start_date, end_date, rentable_types[0], rentable=rentables[4], fixed=True)
    possible, new_situation = check_fixed_booking(new_booking)
    print(possible)

    if new_situation is not None:
        print('possible')
        evaluate.visualize(new_situation)


if __name__ == '__main__':
    # main()
    fixed_booking()
