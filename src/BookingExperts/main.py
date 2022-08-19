# -*- coding: utf-8 -*-
import csv
import time

from evaluation_booking import evaluate, visualize, visualize_original_graph
from src.BookingExperts.bruteforce import bruteforce
from src.BookingExperts.data.server_communication import get_bookings, get_rentables, get_rentable_types, \
    filter_bookings_on_type, filter_rentables_on_type, update_multiple_booking_rentables
from vns import variable_neighbourhood_search


def run_vns(bookings):
    for rentable_type in get_rentable_types():
        begin_time = time.time()
        bookings_by_type = filter_bookings_on_type(rentable_type, bookings)
        # visualize_original_graph(bookings_by_type)
        bookings_by_type_dict = { booking.res_id : booking for booking in bookings_by_type }
        gaps, max_gap = evaluate(bookings_by_type_dict)

        heuristic_gapcount, heuristic_max_gap, heuristic_bookings = variable_neighbourhood_search(10, gaps, max_gap, bookings_by_type_dict)
        # heuristic_bookings = bruteforce(bookings_by_type)
        total_time = time.time() - begin_time
        visualize(heuristic_bookings)
        print(f"Computation time for type {rentable_type}:", round(total_time, 2), "seconds")
        update_multiple_booking_rentables(list(heuristic_bookings.values()))

if __name__ == "__main__":
    start_time = time.time()
    bookings = get_bookings()
    run_vns(bookings)
    # run_pareto(file_name)
    # run_beths_utilization(file_name)
    print("Total computation time: ", round(time.time() - start_time, 2), "seconds")
