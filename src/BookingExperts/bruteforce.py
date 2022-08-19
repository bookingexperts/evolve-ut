from src.BookingExperts.evaluation_booking import visualize
from evaluation_booking import evaluate
from support_methods import *
from operators import *


def bruteforce(all_bookings):
    temp_bookings, temp_rentables = create_backup(all_bookings)

    for booking in temp_bookings:
        booking.rentable.remove_from_planning(booking)

    best_gapcount, best_max_gap = evaluate(all_bookings)
    recursive_solution = place(best_gapcount, best_max_gap, temp_bookings[0], temp_bookings)
    if recursive_solution is not None:
        visualize(recursive_solution)

    print(temp_rentables)


def place(best_gapcount, best_max_gap, to_place, bookings):
    current_best_gapcount = best_gapcount
    current_best_max_gap = best_max_gap

    temp_bookings, temp_rentables = create_backup(bookings)
    original_bookings, original_rentables = create_backup(temp_bookings)
    copy_to_place = to_place.deepcopy()
    conflicts = extended_get_conflicts(None, temp_rentables, to_place)

    new_solution = None

    for conflict in conflicts:
        possible_solution = None
        answer_possible = False
        temp_bookings = fill_class_dataset_with_new_data(temp_bookings, original_bookings)
        temp_rentables = fill_rentable_dataset_with_new_data(temp_rentables, original_rentables)
        if len(conflicts[conflict]) == 0:
            copy_to_place.place_rentable(True)
            plan_booking(conflict, copy_to_place)
            temp_bookings.append(copy_to_place)
            temp_temp_bookings = create_backup(temp_bookings)[0]
            temp_bookings.remove(copy_to_place)
            conflict.remove_from_planning(copy_to_place)

            if to_place == bookings[-1]:
                recursive_answer = temp_temp_bookings
            else:
                recursive_answer = place(best_gapcount, best_max_gap, [booking for booking in temp_temp_bookings if
                                                                       booking.res_id == bookings[
                                                                           bookings.index(to_place) + 1].res_id][0],
                                         temp_temp_bookings)

            if recursive_answer is not None:
                answer_possible = True
                possible_solution = create_backup(recursive_answer)[0]
                new_gapcount, max_gap = evaluate(possible_solution)
                if new_gapcount < current_best_gapcount or (
                        new_gapcount == current_best_gapcount and max_gap > current_best_max_gap):
                    new_solution, new_rentables = create_backup(possible_solution)
                    current_best_gapcount = new_gapcount
                    current_best_max_gap = max_gap
                    visualize(recursive_answer)

    return new_solution
