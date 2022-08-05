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


def extended_steepest_descent(objective_gap_count, objective_max_gap, all_bookings):


    nr_swaps = 0
    current_best_gapcount = objective_gap_count
    current_best_max_gap = objective_max_gap
    original_bookings = all_bookings
    temp_bookings = create_backup_solution_bookings(original_bookings)
    current_best_solution_bookings = create_backup_solution_bookings(original_bookings)
    nr_bookings = len(original_bookings)
    rentables = list(set([booking.rentable for booking in all_bookings]))

    for from_booking_iterate in all_bookings:
        temp_bookings = fill_class_dataset_with_new_data(temp_bookings, all_bookings)
        from_booking = create_backup_solution_bookings([from_booking_iterate])[0]
        from_rentable = from_booking.rentable
        temp_bookings = list(filter(lambda booking: booking.booking_id != from_booking_iterate.booking_id, temp_bookings))
        from_booking.rentable.remove_from_planning(from_booking)

        temp_bookings = get_best_swap_descent(objective_gap_count, objective_max_gap, from_booking, temp_bookings, rentables)

        new_gapcount, max_gap = evaluate(temp_bookings)
        if new_gapcount <= current_best_gapcount:
            if new_gapcount == current_best_gapcount and max_gap <= current_best_max_gap:
                pass
            current_best_gapcount = new_gapcount
            current_best_max_gap = max_gap
            current_best_solution_bookings = fill_class_dataset_with_new_data(current_best_solution_bookings, temp_bookings)

    print("Total number of successful swaps:", nr_swaps)
    return current_best_gapcount, current_best_max_gap, current_best_solution_bookings


def get_best_swap_descent(objective_gaps, objective_max_gap, from_booking, remaining_bookings, all_rentables):

    current_best_gapcount = objective_gaps
    current_best_max_gap = objective_max_gap
    temp_bookings = create_backup_solution_bookings(remaining_bookings)
    temp_bookings_original = create_backup_solution_bookings(remaining_bookings)
    current_best_costwise = create_backup_solution_bookings(remaining_bookings)
    copy_from_booking = create_backup_solution_bookings([from_booking])[0]

    temp_rentables = create_backup_solution_rentable(all_rentables)

    conflicts = extended_get_conflicts(copy_from_booking.rentable, temp_rentables, from_booking)
    for conflict in conflicts:
        temp_rentables = fill_rentable_dataset_with_new_data(temp_rentables, all_rentables)
        temp_bookings = fill_class_dataset_with_new_data(temp_bookings, remaining_bookings)
        print("Conflict with rentable: ", conflict.id, conflicts[conflict])
        if len(conflicts[conflict]) == 0:
            # Swap is possible!
            # Endpoint
            plan_booking(conflict, copy_from_booking)
            new_gapcount, max_gap = evaluate(temp_bookings)
            if new_gapcount <= current_best_gapcount:
                if new_gapcount == current_best_gapcount and max_gap <= current_best_max_gap:
                    pass
                current_best_gapcount = new_gapcount
                current_best_max_gap = max_gap
                current_best_costwise = fill_class_dataset_with_new_data(current_best_costwise, temp_bookings)

        else:
            for booking in conflicts[conflict]:
                temp_bookings = list(filter(lambda x: x.booking_id != booking.booking_id, temp_bookings))
                conflict.remove_from_planning(booking)
            plan_booking(conflict, copy_from_booking)
            copy_from_booking.lock_rentable(True)
            temp_bookings.append(copy_from_booking)
            for booking in conflicts[conflict]:
                temp_bookings = get_best_swap_descent(current_best_gapcount, current_best_max_gap, booking,
                                                      temp_bookings,
                                                      all_rentables)
        new_gapcount, max_gap = evaluate(temp_bookings)
        if new_gapcount <= current_best_gapcount:
            if new_gapcount == current_best_gapcount and max_gap <= current_best_max_gap:
                None  # Dont do anything, not better

            current_best_gapcount = new_gapcount
            current_best_max_gap = max_gap
            current_best_costwise = fill_class_dataset_with_new_data(current_best_costwise, temp_bookings)

    return current_best_costwise

    # Remove conflicted booking(s) from schedule
    # Put from_booking in this spot, pin it
    #

















