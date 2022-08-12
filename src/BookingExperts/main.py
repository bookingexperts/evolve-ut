# -*- coding: utf-8 -*-
import time

from evaluation_booking import evaluate, visualize, visualize_original_graph
from src.BookingExperts.data.server_communication import get_bookings, get_rentables, get_rentable_types, \
    filter_bookings_on_type, filter_rentables_on_type
from vns import variable_neighbourhood_search


def run_vns(bookings, rentables):
    for rentable_type in get_rentable_types():
        bookings_by_type = filter_bookings_on_type(rentable_type, bookings)
        gaps, max_gap = evaluate(bookings_by_type)
        heuristic_gapcount, heuristic_max_gap, heuristic_bookings = variable_neighbourhood_search(10, gaps, max_gap, bookings_by_type)
        visualize(heuristic_bookings)

if __name__ == "__main__":
    start_time = time.time()
    file_name = "scenario_BE.txt"
    bookings = get_bookings()
    rentables = list(get_rentables().values())
    run_vns(bookings, rentables)
    # run_pareto(file_name)
    # run_beths_utilization(file_name)
    print("Total computation time: ", round(time.time() - start_time, 2), "seconds")
