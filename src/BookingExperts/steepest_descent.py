import math

from evaluation_booking import evaluate
from support_methods import *
from operators import *

# extended_steepest_descent() is a function that loops through all bookings in given schedule through (all_bookings)
# For which the highest cost improvement is chosen, and returned.
# This highest cost improvement is found by recursively calling get_best_swap_descent()

# iterations = 0


def extended_steepest_descent(objective_gap_count, objective_max_gap, all_bookings):
    current_best_gapcount = objective_gap_count
    current_best_max_gap = objective_max_gap
    original_bookings = all_bookings
    current_best_solution_bookings, rentables = create_backup(original_bookings)
    rentable_amount = len(rentables)
    recursive_depth = round(math.log(500, rentable_amount-1), 0)
    print(recursive_depth)


    for from_booking_iterate in all_bookings:
        # print("Branch: move", from_booking_iterate.res_id, "to different rentable")
        temp_bookings, temp_rentables = create_backup(all_bookings)
        from_booking = [booking for booking in temp_bookings if booking.res_id == from_booking_iterate.res_id][0]

        temp_bookings.remove(from_booking)
        temp_rentable = from_booking.rentable
        temp_rentable.remove_from_planning(from_booking)
        recursive_answer = get_best_swap_descent(current_best_gapcount, current_best_max_gap, from_booking,
                                                 temp_bookings,
                                                 recursive_depth)

        temp_bookings.append(from_booking)
        plan_booking(temp_rentable, from_booking)
        if recursive_answer is None:
            continue

        else:
            new_gapcount, max_gap = evaluate(recursive_answer)
            if new_gapcount < current_best_gapcount or (
                    new_gapcount == current_best_gapcount and max_gap > current_best_max_gap):
                current_best_gapcount = new_gapcount
                current_best_max_gap = max_gap

                for booking in recursive_answer:
                    booking.place_rentable(False)

                # print("New best solution found:", current_best_gapcount, current_best_max_gap)
                # for booking in recursive_answer:
                #     for booking_og in all_bookings:
                #         if booking.res_id == booking_og.res_id and booking.rentable.rentable_id != booking_og.rentable.rentable_id:
                #             print(booking.res_id, booking.start_date, booking.end_date)
                #             break

                current_best_solution_bookings = create_backup(recursive_answer)[0]
    # print('iterations:', iterations)
    return current_best_gapcount, current_best_max_gap, current_best_solution_bookings


def get_best_swap_descent(objective_gaps, objective_max_gap, from_booking, remaining_bookings, depth):
    # global iterations
    # iterations += 1
    if depth < 1:
        return None
    current_best_gapcount = objective_gaps
    current_best_max_gap = objective_max_gap
    temp_bookings, temp_rentables = create_backup(remaining_bookings)

    original_bookings, original_rentables = create_backup(temp_bookings)
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
            temp_bookings.append(copy_from_booking)
            possible_solution = create_backup(temp_bookings)[0]
            temp_bookings.remove(copy_from_booking)
            conflict.remove_from_planning(copy_from_booking)

        else:
            for booking in conflicts[conflict]:
                temp_bookings = list(filter(lambda x: x.res_id != booking.res_id, temp_bookings))
                conflict.remove_from_planning(booking)

            copy_from_booking.place_rentable(True)
            plan_booking(conflict, copy_from_booking)
            temp_bookings.append(copy_from_booking)
            temp_temp_bookings = create_backup(temp_bookings)[0]

            for booking in conflicts[conflict]:
                recursive_answer = get_best_swap_descent(current_best_gapcount, current_best_max_gap, booking,
                                                         temp_temp_bookings, depth - 1)
                if recursive_answer is None:
                    answer_possible = False
                    break
                else:
                    for booking1 in recursive_answer:
                        for booking2 in temp_bookings:
                            if booking1.res_id == booking2.res_id != booking.res_id and booking1.placed and not booking2.placed:
                                booking1.place_rentable(False)
                                break

                    temp_temp_bookings = recursive_answer
                    answer_possible = True
                    [booking_placed for booking_placed in recursive_answer if booking_placed.res_id == booking.res_id][0].place_rentable(True)
            for booking1 in conflicts[conflict]:
                for booking2 in temp_temp_bookings:
                    if booking1.res_id == booking2.res_id:
                        booking2.place_rentable(False)
            conflict.remove_from_planning(copy_from_booking)

            if answer_possible:
                possible_solution = create_backup_solution_bookings(temp_temp_bookings)
            for booking in conflicts[conflict]:
                plan_booking(conflict, booking)
                temp_bookings.append(booking)

        copy_from_booking.place_rentable(False)
        temp_bookings = list(
            filter(lambda remove_booking: remove_booking.res_id != copy_from_booking.res_id, temp_bookings))
        if not answer_possible:
            continue
        if possible_solution is not None:
            temp_copy_from_booking = \
                [booking for booking in possible_solution if booking.res_id == copy_from_booking.res_id][0]
            temp_copy_from_booking.place_rentable(False)


            new_gapcount, max_gap = evaluate(possible_solution)
            if new_gapcount < current_best_gapcount or (
                    new_gapcount == current_best_gapcount and max_gap > current_best_max_gap):
                new_solution, new_rentables = create_backup(possible_solution)
                current_best_gapcount = new_gapcount
                current_best_max_gap = max_gap
    if new_solution is not None:
        return new_solution
    else:
        return None

