# -*- coding: utf-8 -*-
import time

# from Assignment2.beths_utilization import run_beths_utilization
from pareto import pareto_search
import booking
import rentable
from vns import variable_neighbourhood_search
from schedule_obtain import first_come_first_serve
from evaluation_booking import evaluate, visualize


# def run_vns(file):
#     pseudo_berths, pseudo_vessels = first_come_first_serve(file)
#     heuristic_costs, heuristic_vessels = variable_neighborhood_search(10, evaluate(pseudo_vessels), pseudo_vessels)
#     visualize(heuristic_vessels)

def run_vns(bookings, rentables):
    for rentable_type in rentable.get_rentable_types():
        pseudo_rentables, pseudo_bookings = first_come_first_serve(booking.filter_on_type(rentable_type, bookings),
                                                                   rentable.filter_on_type(rentable_type, rentables))
        visualize(pseudo_bookings)
        heuristic_costs, heuristic_bookings = variable_neighbourhood_search(1, evaluate(pseudo_bookings),
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
    bookings = booking.get_bookings()
    rentables = list(rentable.get_rentables().values())
    run_vns(bookings, rentables)
    # run_pareto(file_name)
    # run_beths_utilization(file_name)
    print("Total computation time: ", round(time.time() - start_time, 2), "seconds")
