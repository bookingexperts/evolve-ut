# Create a set of vessels with the characteristics of the other solution
import itertools
import random


def create_backup_solution_bookings(set_of_bookings):
    copy_of_bookings = []
    for booking in set_of_bookings:
        copy_of_bookings.append(booking.deepcopy())
    return copy_of_bookings


def create_backup_solution_rentable(set_of_rentables):
    copy_of_rentables = []
    for rentable in set_of_rentables:
        copy_of_rentables.append(rentable.deepcopy())
    return copy_of_rentables


def fill_class_dataset_with_new_data(old_class_set, new_class_set):
    for old_item in old_class_set:
        for new_item in new_class_set:
            if old_item.res_id == new_item.res_id:
                old_item.start_date = new_item.start_date
                old_item.end_date = new_item.end_date
                old_item.rentable.schedule = new_item.rentable.schedule
                old_item.rentable_type = new_item.rentable_type
                old_item.fixed = new_item.fixed
                old_item.placed = new_item.placed
                break
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


def fill_rentable_dataset_with_new_data(old_rentable_set, new_rentable_set):
    for old_item in old_rentable_set:
        for new_item in new_rentable_set:
            if old_item.rentable_id == new_item.rentable_id:
                old_item.opening_date = new_item.opening_date
                old_item.closing_date = new_item.closing_date
                old_item.type = new_item.type
                old_item.schedule = new_item.schedule
                break
    return old_rentable_set


def plan_booking(rentable, booking):
    rentable.fill_planning(booking)
    booking.stay_start(rentable)
    # print("Booking", booking.res_id, "placed for", booking.start_date, "until", booking.end_date, "on rentable", rentable.rentable_id, "\n")

