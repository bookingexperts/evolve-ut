from evaluation_booking import evaluate
from support_methods import *
from operators import *
from copy import deepcopy


def extended_steepest_descent(objective_gap_count, objective_max_gap, all_bookings):
    current_best_gapcount = objective_gap_count
    current_best_max_gap = objective_max_gap
    original_bookings = all_bookings
    temp_bookings, rentables = create_backup(original_bookings,
                                             set([booking.rentable for booking in original_bookings]))
    current_best_solution_bookings = create_backup_solution_bookings(original_bookings)

    for from_booking_iterate in all_bookings:
        # print(current_best_gapcount, current_best_max_gap)
        print("Branch: move", from_booking_iterate.res_id, "to different rentable")
        temp_bookings, temp_rentables = create_backup(all_bookings, set([booking.rentable for booking in all_bookings]))
        from_booking = [booking for booking in temp_bookings if booking.res_id == from_booking_iterate.res_id][0]
        # # temp_bookings = fill_class_dataset_with_new_data(temp_bookings, original_bookings)
        # temp_rentables = list(set([booking.rentable for booking in temp_bookings]))
        # for booking in temp_bookings:
        #     for rentable in temp_rentables:
        #         if booking.rentable.rentable_id == rentable.rentable_id:
        #             booking.rentable = rentable
        #             break
        # from_booking = [booking for booking in temp_bookings if booking.id == from_booking_iterate.id][0]
        temp_bookings.remove(from_booking)
        # temp_bookings = list(filter(lambda booking: booking.booking_id != from_booking_iterate.booking_id, temp_bookings))
        # temp_rentable = list(filter(lambda rentable: rentable.rentable_id == from_booking.rentable.rentable_id, temp_rentables))[0]
        temp_rentable = from_booking.rentable
        # temp_rentable.remove_from_planning([booking for booking in temp_rentable.schedule.values() if booking.id == from_booking.id][0])
        # print(not all(date in temp_rentable.schedule for date in daterange(from_booking.start_date, from_booking.end_date)))
        schedule = temp_rentable.schedule
        temp_rentable.remove_from_planning(from_booking)
        recursive_answer = get_best_swap_descent(current_best_gapcount, current_best_max_gap, from_booking,
                                                 temp_bookings,
                                                 1)

        temp_bookings.append(from_booking)
        plan_booking(temp_rentable, from_booking)
        if recursive_answer is None:
            continue
        else:

            new_gapcount, max_gap = evaluate(recursive_answer)
            # print(new_gapcount, max_gap)
            if new_gapcount < current_best_gapcount or (
                    new_gapcount == current_best_gapcount and max_gap > current_best_max_gap):
                current_best_gapcount = new_gapcount
                current_best_max_gap = max_gap
                # current_best_solution_bookings = fill_class_dataset_with_new_data(current_best_solution_bookings, recursive_answer)
                for booking in recursive_answer:
                    booking.place_rentable(False)
                    for booking_og in original_bookings:
                        if booking.booking_id == booking_og.booking_id and booking.rentable.rentable_id != booking_og.rentable.rentable_id:
                            print(booking.res_id)
                placed_len = [booking for booking in recursive_answer if booking.placed and not booking.fixed]

                print("New best solution found:", current_best_gapcount, current_best_max_gap)
                current_best_solution_bookings = deepcopy(recursive_answer)
    return current_best_gapcount, current_best_max_gap, current_best_solution_bookings


def get_best_swap_descent(objective_gaps, objective_max_gap, from_booking, remaining_bookings, depth):
    if depth > 4:
        return None
    current_best_gapcount = objective_gaps
    current_best_max_gap = objective_max_gap
    temp_bookings, temp_rentables = create_backup(remaining_bookings,
                                                  set([booking.rentable for booking in remaining_bookings]))

    original_bookings, original_rentables = create_backup(temp_bookings, temp_rentables)
    copy_from_booking = from_booking.deepcopy()

    new_solution = None
    # temp_rentables = {}
    # for booking in temp_bookings:
    #     temp_rentables[booking.rentable.rentable_id] = booking.rentable
    # temp_rentables = list(temp_rentables.values())

    conflicts = extended_get_conflicts(from_booking.rentable, temp_rentables, from_booking)
    # print("Booking", from_booking.res_id, "has conflicts:", conflicts)
    if len(conflicts) == 0:
        # print("No swap possible anymore for", from_booking.res_id)
        # print("<")
        return None
    for conflict in conflicts:
        possible_solution = None
        answer_possible = False
        temp_bookings = fill_class_dataset_with_new_data(temp_bookings, remaining_bookings)
        temp_rentables = fill_rentable_dataset_with_new_data(temp_rentables, original_rentables)
        rentable_to = conflict.deepcopy()
        if len(conflicts[conflict]) == 0:
            answer_possible = True
            # print("No conflict, place", from_booking.res_id, "at rentable", conflict.rentable_id)
            # Swap is possible!
            # Endpoint
            if len(list(filter(lambda x: x.res_id == copy_from_booking.res_id, temp_bookings))) > 0:
                None
            copy_from_booking.place_rentable(True)
            plan_booking(conflict, copy_from_booking)
            possible_solution = create_backup(temp_bookings, temp_rentables)[0]
            possible_solution.append(copy_from_booking)
            possible_string = "Solution found by displacing: "
            for booking in possible_solution:
                if booking.placed and not booking.fixed:
                    possible_string += str(booking.res_id) + " "
            # print(possible_string)

            # print("New optimal situation found!")
        else:
            # print("Booking", from_booking.res_id, " has conflict with rentable:", conflict.res_id, conflicts[conflict])
            for booking in conflicts[conflict]:
                # print("Removing booking", booking.res_id, "from ", booking.rentable.rentable_id)
                temp_bookings = list(filter(lambda x: x.res_id != booking.res_id, temp_bookings))
                conflict.remove_from_planning(booking)
            copy_from_booking.place_rentable(True)
            plan_booking(conflict, copy_from_booking)
            temp_bookings.append(copy_from_booking)
            temp_temp_bookings = create_backup_solution_bookings(temp_bookings)
            for booking in conflicts[conflict]:
                # print("Attempting to place booking", booking.res_id, "..... (" + str(booking.start_date) + " to " + str(booking.end_date) + ")" )
                # print(">")
                recursive_answer = get_best_swap_descent(current_best_gapcount, current_best_max_gap, booking,
                                                         temp_temp_bookings, depth + 1)

                if recursive_answer is None:
                    answer_possible = False

                    # for booking_back in conflicts[conflict]:
                    #     plan_booking(conflict, booking_back)
                    #     temp_bookings.append(booking_back)
                    break
                else:
                    placed_len = [booking for booking in recursive_answer if booking.placed and not booking.fixed]
                    for booking1 in recursive_answer:
                        for booking2 in temp_bookings:
                            if booking1.res_id == booking2.res_id != booking.res_id and booking1.placed and not booking2.placed:
                                booking1.place_rentable(False)

                    temp_temp_bookings = recursive_answer
                    answer_possible = True
                    [booking_placed for booking_placed in recursive_answer if booking_placed.res_id == booking.res_id][0].place_rentable(True)
            copy_from_booking.place_rentable(False)
            if answer_possible:
                possible_solution = create_backup_solution_bookings(temp_temp_bookings)
            # print("_")
            temp_bookings = list(filter(lambda remove_booking: remove_booking.res_id != copy_from_booking.res_id, temp_bookings))
            conflict.remove_from_planning(copy_from_booking)

            for booking in conflicts[conflict]:
                plan_booking(conflict, booking)
                temp_bookings.append(booking)
        if not answer_possible:
            continue
        if possible_solution is not None:

            new_gapcount, max_gap = evaluate(possible_solution)
            # print(new_gapcount, max_gap)
            if new_gapcount < current_best_gapcount or (
                    new_gapcount == current_best_gapcount and max_gap > current_best_max_gap):
                new_solution, new_rentables = create_backup(possible_solution, set(booking.rentable for booking in possible_solution))
                # print(new_gapcount, max_gap)
    # print("<")
    if new_solution is not None:
        return new_solution
    else:
        return None
    # Remove conflicted booking(s) from schedule
    # Put from_booking in this spot, pin it
    #


def get_schedule_ready(bookings):
    pass
