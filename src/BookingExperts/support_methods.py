# Create a set of vessels with the characteristics of the other solution
import copy
import itertools
import random


def create_backup_solution_bookings(set_of_bookings):
    return copy.deepcopy(set_of_bookings)


def create_backup_solution_rentable(set_of_rentables):
    copy_of_rentables = []
    for rentable in set_of_rentables:
        copy_of_rentables.append(rentable.deepcopy())
    return copy_of_rentables


def fill_class_dataset_with_new_data(old_class_set, new_class_set):
    for item in old_class_set:
        old_class_set[item].start_date = new_class_set[item].start_date
        old_class_set[item].end_date = new_class_set[item].end_date
        old_class_set[item].rentable.schedule = new_class_set[item].rentable.schedule
        old_class_set[item].rentable_type = new_class_set[item].rentable_type
        old_class_set[item].fixed = new_class_set[item].fixed
        old_class_set[item].placed = new_class_set[item].placed
        old_class_set[item].cant_be_moved = old_class_set[item].cant_be_moved
    return old_class_set


def create_backup(bookings):
    backup_rentables = {}
    backup_bookings = {}

    for booking in bookings:
        backup_bookings[booking.res_id] = booking.deepcopy()

    rentables = set([booking.rentable for booking in backup_bookings.values()])

    for rentable in rentables:
        backup_rentables[rentable.rentable_id] = rentable
        for date in rentable.schedule:
            rentable.schedule[date] = backup_bookings[rentable.schedule[date].res_id]

    for booking in backup_bookings.values():
        booking.rentable = backup_rentables[booking.rentable.rentable_id]


    return list(backup_bookings.values()), list(backup_rentables.values())


def create_backup_new(bookings):
    backup_bookings = copy.deepcopy(bookings)
    rentables = { booking.rentable.rentable_id : booking.rentable for booking in backup_bookings.values() }



    for rentable in rentables.values():
        for date in rentable.schedule:
            rentable.schedule[date] = backup_bookings[rentable.schedule[date].res_id]

    for booking in backup_bookings.values():
        booking.rentable = rentables[booking.rentable.rentable_id]

    return backup_bookings, rentables


def fill_rentable_dataset_with_new_data(old_rentable_set, new_rentable_set):
    for item in old_rentable_set:
        old_rentable_set[item].opening_date = new_rentable_set[item].opening_date
        old_rentable_set[item].closing_date = new_rentable_set[item].closing_date
        old_rentable_set[item].type = new_rentable_set[item].type
        old_rentable_set[item].schedule = new_rentable_set[item].schedule
    return old_rentable_set


def plan_booking(rentable, booking):
    rentable.fill_planning(booking)
    booking.stay_start(rentable)
    # print("Booking", booking.res_id, "placed for", booking.start_date, "until", booking.end_date, "on rentable", rentable.rentable_id, "\n")

