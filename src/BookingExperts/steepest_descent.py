from evaluation_booking import evaluate
from src.BookingExperts.operators import swap_bookings_in_schedule
from support_methods import *
from operators import *


# Find all possible swaps of vessels that would improve the costs. At the end, return the best solution (the one with
# the steepest descent)
def steepest_descent(objective_value, all_bookings):
    nr_swaps = 0
    current_best = objective_value
    original_bookings = all_bookings
    temp_bookings = create_backup_solution_bookings(original_bookings)
    current_best_solution_bookings = create_backup_solution_bookings(original_bookings)
    nr_bookings = len(original_bookings)
    for from_booking_id in range(nr_bookings):
        for to_booking_id in range(from_booking_id, nr_bookings):
            temp_bookings = fill_class_dataset_with_new_data(temp_bookings, original_bookings)
            from_booking = temp_bookings[from_booking_id]
            to_booking = temp_bookings[to_booking_id]

            if check_swap_possibility(from_booking.rentable, to_booking.rentable, from_booking, to_booking):
                swap_bookings_in_schedule(from_booking.rentable, to_booking.rentable, from_booking, to_booking)
                costs = evaluate(temp_bookings)
                if costs < current_best:
                    nr_swaps += 1
                    current_best = costs
                    current_best_solution_bookings = fill_class_dataset_with_new_data(current_best_solution_bookings, temp_bookings)

    print("Total number of successful swaps:", nr_swaps)
    return current_best, current_best_solution_bookings


def extended_steepest_descent(objective_value, all_bookings):


    nr_swaps = 0
    current_best = objective_value
    original_bookings = all_bookings
    temp_bookings = create_backup_solution_bookings(original_bookings)
    current_best_solution_bookings = create_backup_solution_bookings(original_bookings)
    nr_bookings = len(original_bookings)
    rentables = set([booking.rentable for booking in all_bookings])

    for from_booking in all_bookings:
        schedules = []
        conflicts = extended_get_conflicts(from_booking.rentable, rentables, from_booking)

        for conflict in conflicts:
            print(conflict, conflicts[conflict])
            if len(conflicts[conflict]) == 0:
                None
                # Swap is possible!
                # Endpoint
            else:
                None
                # Remove conflicted booking(s) from schedule
                # Put from_booking in this spot, pin it
                #

        for to_booking in to_bookings:

            temp_bookings = fill_class_dataset_with_new_data(temp_bookings, original_bookings)
            from_booking = temp_bookings[from_booking]
            to_booking = temp_bookings[to_booking]

            if check_extended_swap_possibility(to_booking.rentable, to_booking, rentables, temp_bookings.delete(to_booking)):

                extended_steepest_descent(objective_value, temp_bookings.delete(to_booking))

                costs = evaluate(temp_bookings)
            if check_swap_possibility(from_booking.rentable, to_booking.rentable, from_booking, to_booking):
                swap_bookings_in_schedule(from_booking.rentable, to_booking.rentable, from_booking, to_booking)
                costs = evaluate(temp_bookings)
                if costs < current_best:
                    nr_swaps += 1
                    current_best = costs
                    current_best_solution_bookings = fill_class_dataset_with_new_data(current_best_solution_bookings, temp_bookings)

    print("Total number of successful swaps:", nr_swaps)
    return current_best, current_best_solution_bookings


def get_best_swap_descent(og_val, from_booking, remaining_bookings, all_rentables):

    current_best_cost = og_val
    temp_bookings = create_backup_solution_bookings(remaining_bookings)
    temp_bookings_original = create_backup_solution_bookings(remaining_bookings)
    current_best_costwise = create_backup_solution_bookings(remaining_bookings)
    copy_from_booking = create_backup_solution_bookings([from_booking])[0]

    temp_rentables = create_backup_solution_rentable(all_rentables)

    conflicts = extended_get_conflicts(copy_from_booking.rentable, temp_rentables, from_booking)
    for conflict in conflicts:
        temp_bookings = fill_class_dataset_with_new_data(temp_bookings, remaining_bookings)
        print(conflict, conflicts[conflict])
        if len(conflicts[conflict]) == 0:
            None
            # Swap is possible!
            # Endpoint
            plan_booking(conflict, copy_from_booking)
            new_cost = evaluate(temp_bookings)
            if new_cost < current_best_cost:
                current_best_cost = new_cost
                current_best_costwise = fill_class_dataset_with_new_data(current_best_costwise, temp_bookings)
        else:
            for booking in conflicts[conflict]:
                temp_bookings.remove(booking)
            plan_booking(conflict, copy_from_booking)
            for booking in conflicts[conflict]:
                temp_bookings = get_best_swap_descent(booking,
                                                      temp_bookings,
                                                      all_rentables)
                return temp_bookings

    return

    # Remove conflicted booking(s) from schedule
    # Put from_booking in this spot, pin it
    #

















