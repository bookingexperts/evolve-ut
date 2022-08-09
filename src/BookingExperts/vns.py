from evaluation_booking import evaluate, visualize
from steepest_descent import steepest_descent, extended_steepest_descent
from support_methods import *


def variable_neighbourhood_search(nr_of_iterations, objective_gapcount, objective_max_gap, all_bookings):
    best_bookings = all_bookings
    best_gapcount = objective_gapcount
    best_max_gap = objective_max_gap
    iteration = 0
    #Calculate an optimum with the current solution
    while True:
        iteration += 1
        print("Calculate local optimum")

        extended_gapcount, extended_max_gap, extended_bookings = extended_steepest_descent(best_gapcount, best_max_gap, all_bookings)
        if (extended_gapcount, extended_max_gap) == (best_gapcount, best_max_gap):
            break
        best_gapcount = extended_gapcount
        best_max_gap = extended_max_gap
        print(best_gapcount, best_max_gap)


    visualize(best_bookings)
    return best_gapcount, best_max_gap, best_bookings