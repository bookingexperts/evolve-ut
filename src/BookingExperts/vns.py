from evaluation_booking import evaluate
from steepest_descent import steepest_descent
from support_methods import *


def variable_neighbourhood_search(nr_of_iterations, objective_value, all_rentables, all_bookings):
    best_bookings = all_bookings
    best_rentables = all_rentables
    best_cost = objective_value
    iteration = 0
    #Calculate an optimum with the current solution
    while True:
        iteration += 1
        print("Calculate local optimum")
        new_costs, new_bookings, new_rentables = steepest_descent(best_cost, best_bookings, best_rentables)

















def variable_neighborhood_search(nr_of_iterations, objective_value, all_vessels):
    best_vessels = all_vessels
    best_costs = objective_value
    iteration = 0
    # Calculate an optimum with the current solution
    while True:
        iteration += 1
        print("Calculate local optimum")
        new_costs, new_vessels = steepest_descent(best_costs, best_vessels)
        if best_costs == new_costs:
            break
        best_vessels = new_vessels
        best_costs = new_costs

    print(best_costs)

    # Start looking for new neighborhoods and check if their solution is better
    original_vessels = best_vessels
    best_vessels = create_backup_solution_vessels(original_vessels)
    iteration = 0
    while iteration < nr_of_iterations:
        iteration += 1
        print("Iteration ", iteration)
        temp_vessels = create_backup_solution_vessels(original_vessels)
        swap_vessels = random.sample(temp_vessels, k=2)
        # Try to find two vessels that can be swapped before continuing.
        while not check_swap_possibility(swap_vessels[0].helped_by_berth, swap_vessels[1].helped_by_berth,
                                         swap_vessels[0], swap_vessels[1]):
            swap_vessels = random.sample(all_vessels, k=2)
        # Swap the two vessels
        swap_ships_in_schedule(swap_vessels[0].helped_by_berth, swap_vessels[1].helped_by_berth,
                               swap_vessels[0], swap_vessels[1])

        best_costs_new_neighbor = evaluate(temp_vessels)
        # As long as the new solution is better than the best_seen solution so far, try to improve
        while True:
            new_costs, new_vessels = steepest_descent(best_costs_new_neighbor, temp_vessels)
            if new_costs == best_costs_new_neighbor:
                break
            best_costs_new_neighbor = new_costs
            temp_vessels = fill_class_dataset_with_new_data(temp_vessels, new_vessels)
        # If the newly found solution is the best so far, update the best solution
        if new_costs < best_costs:
            print(new_costs)
            print(best_costs)
            best_vessels = fill_class_dataset_with_new_data(best_vessels, temp_vessels)
            best_costs = new_costs
            original_vessels = fill_class_dataset_with_new_data(original_vessels, best_vessels)
    # Return the overall best solution with its costs.
    return best_costs, best_vessels
