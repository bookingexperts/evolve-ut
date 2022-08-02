# -*- coding: utf-8 -*-
import time

from Assignment2.beths_utilization import run_beths_utilization
from Assignment2.pareto import pareto_search
from Assignment2.vns import variable_neighborhood_search
from fcfs import first_come_first_serve
from evaluation_booking import evaluate, visualize, calculate_makespan


def run_vns(file):
    pseudo_berths, pseudo_vessels = first_come_first_serve(file)
    heuristic_costs, heuristic_vessels = variable_neighborhood_search(10, evaluate(pseudo_vessels), pseudo_vessels)
    visualize(heuristic_vessels)


def run_pareto(file):
    pareto_solutions = pareto_search(file)
    # Print the details of all solutions in the pareto set.
    for i, solution in enumerate(pareto_solutions):
        print("Solution ", i + 1, ": ")
        print("Costs: €", evaluate(solution))
        print("Makespan: ", calculate_makespan(solution))


if __name__ == "__main__":
    start_time = time.time()
    file_name = "Data/scenario_BE.txt"
    run_vns(file_name)
    # run_pareto(file_name)
    # run_beths_utilization(file_name)
    print("Total computation time: ", round(time.time() - start_time, 2), "seconds")

