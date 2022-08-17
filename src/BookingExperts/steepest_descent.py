import math

from evaluation_booking import evaluate
from support_methods import *
from operators import *

# extended_steepest_descent() is a function that loops through all bookings in given schedule through (all_bookings)
# For which the highest cost improvement is chosen, and returned.
# This highest cost improvement is found by recursively calling get_best_swap_descent()


def extended_steepest_descent(objective_gap_count, objective_max_gap, all_bookings):
    current_best_gapcount = objective_gap_count
    current_best_max_gap = objective_max_gap
    original_bookings = all_bookings
    current_best_solution_bookings, rentables = create_backup_new(original_bookings)
    rentable_amount = len(rentables)
    recursive_depth = round(math.log(500, rentable_amount-1), 0)


    for from_booking_iterate in all_bookings:
        if all_bookings[from_booking_iterate].cant_be_moved:
            # print(from_booking_iterate.res_id, "is fixed.")
            continue
        # print("Branch: move", from_booking_iterate.res_id, "to different rentable")
        temp_bookings, temp_rentables = create_backup_new(all_bookings)

        from_booking = temp_bookings[from_booking_iterate]
        del temp_bookings[from_booking_iterate]
        temp_rentable = from_booking.rentable
        temp_rentable.remove_from_planning(from_booking)

        recursive_answer = get_best_swap_descent(current_best_gapcount, current_best_max_gap, from_booking,
                                                 temp_bookings,
                                                 recursive_depth-1)

        temp_bookings[from_booking_iterate] = from_booking
        plan_booking(temp_rentable, from_booking)
        if recursive_answer is None:
            continue

        else:
            new_gapcount, max_gap = evaluate(recursive_answer)
            if new_gapcount < current_best_gapcount or (
                    new_gapcount == current_best_gapcount and max_gap > current_best_max_gap):
                current_best_gapcount = new_gapcount
                current_best_max_gap = max_gap

                for booking in recursive_answer.values():
                    booking.place_rentable(False)

                current_best_solution_bookings = create_backup_new(recursive_answer)[0]
    return current_best_gapcount, current_best_max_gap, current_best_solution_bookings


def get_best_swap_descent(objective_gaps, objective_max_gap, from_booking, remaining_bookings, depth):
    if depth < 1:
        return None
    current_best_gapcount = objective_gaps
    current_best_max_gap = objective_max_gap
    temp_bookings, temp_rentables = create_backup_new(remaining_bookings)

    original_bookings, original_rentables = create_backup_new(temp_bookings)
    copy_from_booking = from_booking.deepcopy()

    new_solution = None

    conflicts = extended_get_conflicts(from_booking.rentable, temp_rentables, from_booking)
    if len(conflicts) == 0:
        return None

    for conflict in conflicts:
        possible_solution = None
        answer_possible = False
        temp_bookings = fill_class_dataset_with_new_data(temp_bookings, remaining_bookings)
        temp_rentables = fill_rentable_dataset_with_new_data(temp_rentables, original_rentables)
        if len(conflicts[conflict]) == 0:
            answer_possible = True
            # Swap is possible!
            # Endpoint
            copy_from_booking.place_rentable(True)
            plan_booking(conflict, copy_from_booking)
            temp_bookings[copy_from_booking.res_id] = copy_from_booking
            possible_solution = create_backup_new(temp_bookings)[0]
            conflict.remove_from_planning(copy_from_booking)

        elif depth == 1:
            continue

        else:
            for booking in conflicts[conflict]:
                del temp_bookings[booking.res_id]
                conflict.remove_from_planning(booking)

            copy_from_booking.place_rentable(True)
            plan_booking(conflict, copy_from_booking)
            temp_bookings[copy_from_booking.res_id] = copy_from_booking
            temp_temp_bookings = create_backup_new(temp_bookings)[0]

            for booking in conflicts[conflict]:
                recursive_answer = get_best_swap_descent(current_best_gapcount, current_best_max_gap, booking,
                                                         temp_temp_bookings, depth - 1)
                if recursive_answer is None:
                    answer_possible = False
                    break
                else:
                    for sol_booking_id in recursive_answer:

                        if sol_booking_id != booking.res_id and \
                                recursive_answer[sol_booking_id].placed and not temp_bookings[sol_booking_id].placed:
                            recursive_answer[sol_booking_id].place_rentable(False)
                            break

                    temp_temp_bookings = recursive_answer
                    answer_possible = True

            for booking in conflicts[conflict]:
                if booking.res_id in temp_temp_bookings:
                    temp_temp_bookings[booking.res_id].place_rentable(False)
            conflict.remove_from_planning(copy_from_booking)

            if answer_possible:
                possible_solution = create_backup_solution_bookings(temp_temp_bookings)
            for booking in conflicts[conflict]:
                plan_booking(conflict, booking)
                temp_bookings[booking.res_id] = booking

        copy_from_booking.place_rentable(False)
        del temp_bookings[copy_from_booking.res_id]

        if answer_possible:
            possible_solution[copy_from_booking.res_id].place_rentable(False)

            new_gapcount, max_gap = evaluate(possible_solution)
            if new_gapcount < current_best_gapcount or (
                    new_gapcount == current_best_gapcount and max_gap > current_best_max_gap):
                new_solution, new_rentables = create_backup_new(possible_solution)
                current_best_gapcount = new_gapcount
                current_best_max_gap = max_gap

    if new_solution is not None:
        return new_solution
    else:
        return None

