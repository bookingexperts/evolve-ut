import csv
import time

from evaluation_booking import evaluate, visualize
from steepest_descent import extended_steepest_descent
from support_methods import *


def variable_neighbourhood_search(nr_of_iterations, objective_gapcount, objective_max_gap, all_bookings):
    # filename = f'{str(list(all_bookings.values())[0].rentable.type)}_times'
    # file = open('C:/Users/barry/Documents/University/CS/Minor/study tour/CR/evolve-ut/src/BookingExperts/Benchmark/' + filename + '_5.csv', 'w')
    # writer = csv.writer(file)

    best_gapcount = objective_gapcount
    best_max_gap = objective_max_gap
    best_bookings = create_backup_solution_bookings(all_bookings)
    visualize(all_bookings)
    iteration = 0
    # Calculate an optimum with the current solution
    while True:
        start_time = time.time()
        iteration += 1
        print("Calculate local optimum")

        extended_gapcount, extended_max_gap, extended_bookings = extended_steepest_descent(best_gapcount, best_max_gap, best_bookings)

        if extended_bookings is None or (extended_gapcount, extended_max_gap) == (best_gapcount, best_max_gap):
            # writer.writerow([extended_gapcount, extended_max_gap, round(time.time() - start_time, 2)])
            # file.close()
            break

        visualize(extended_bookings)

        if (extended_gapcount, extended_max_gap) == (best_gapcount, best_max_gap):
            break
        best_gapcount = extended_gapcount
        best_max_gap = extended_max_gap
        best_bookings = extended_bookings
        # writer.writerow([extended_gapcount, extended_max_gap, round(time.time() - start_time, 2)])
        print(best_gapcount, best_max_gap)

    # visualize(best_bookings)
    return best_gapcount, best_max_gap, best_bookings
