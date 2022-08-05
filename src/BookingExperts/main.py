# -*- coding: utf-8 -*-
import time

from data import rentable
from evaluation_booking import evaluate, visualize
from pareto import pareto_search
from schedule_obtain import first_come_first_serve
from src.BookingExperts.data.server_communication import get_bookings, get_rentables, get_rentable_types, \
    filter_bookings_on_type, filter_rentables_on_type
from vns import variable_neighbourhood_search


def run_vns(bookings, rentables):
    for rentable_type in get_rentable_types():
        pseudo_rentables, pseudo_bookings = first_come_first_serve(filter_bookings_on_type(rentable_type, bookings),
                                                                   filter_rentables_on_type(rentable_type, rentables))
        visualize(pseudo_bookings)
        gaps, max_gap = evaluate(pseudo_bookings)
        heuristic_costs, heuristic_bookings = variable_neighbourhood_search(10, gaps, max_gap,
                                                                            pseudo_bookings)
        visualize(heuristic_bookings)


def run_pareto(file):
    pareto_solutions = pareto_search(file)
    # Print the details of all solutions in the pareto set.
    for i, solution in enumerate(pareto_solutions):
        print("Solution ", i + 1, ": ")
        print("Gaps: ", evaluate(solution))


if __name__ == "__main__":
    start_time = time.time()
    file_name = "scenario_BE.txt"
    bookings = get_bookings()
    rentables = list(get_rentables().values())
    run_vns(bookings, rentables)
    # run_pareto(file_name)
    # run_beths_utilization(file_name)
    print("Total computation time: ", round(time.time() - start_time, 2), "seconds")
