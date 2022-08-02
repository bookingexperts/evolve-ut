from evaluation_booking import evaluate
from src.BookingExperts.operators import swap_bookings_in_schedule
from support_methods import *


# Find all possible swaps of vessels that would improve the costs. At the end, return the best solution (the one with
# the steepest descent)
def steepest_descent(objective_value, all_rentables, all_bookings):
    nr_swaps = 0
    current_best = objective_value
    original_bookings = all_bookings
    original_rentables = all_rentables

    temp_bookings = create_backup_solution_bookings(original_bookings)
    current_best_solution_bookings = create_backup_solution_bookings(original_bookings)
    nr_bookings = len(original_bookings)
    for from_booking_id in range(nr_bookings):
        for to_booking_id in range(from_booking_id, nr_bookings):
            temp_bookings = fill_class_dataset_with_new_data(temp_bookings, original_bookings)
            from_booking = temp_bookings[from_booking_id]
            to_booking= temp_bookings[to_booking_id]

            if check_swap_possibility(from_booking.housed_by, to_booking.housed_by, from_booking, to_booking):
                swap_bookings_in_schedule(from_booking.housed_by, to_booking.housed_by, from_booking, to_booking)
                costs =


    temp_vessels = create_backup_solution_bookings(original_vessels)
    current_best_solution_vessels = create_backup_solution_bookings(original_vessels)
    nr_vessels = len(original_vessels)
    for from_vessel_id in range(nr_vessels):
        for to_vessel_id in range(from_vessel_id, nr_vessels):
            temp_vessels = fill_class_dataset_with_new_data(temp_vessels, original_vessels)
            from_vessel = temp_vessels[from_vessel_id]
            to_vessel = temp_vessels[to_vessel_id]
            if check_swap_possibility(from_vessel.helped_by_berth, to_vessel.helped_by_berth, from_vessel, to_vessel):
                swap_ships_in_schedule(from_vessel.helped_by_berth, to_vessel.helped_by_berth, from_vessel, to_vessel)
                costs = evaluate(temp_vessels)
                if costs < current_best:
                    nr_swaps += 1
                    current_best = costs
                    current_best_solution_vessels = fill_class_dataset_with_new_data(current_best_solution_vessels,
                                                                                     temp_vessels)
    print("Total number of successful swaps:", nr_swaps)
    return current_best, current_best_solution_vessels
