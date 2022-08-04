from evaluation_booking import evaluate, visualize
from steepest_descent import steepest_descent, extended_steepest_descent
from support_methods import *


def variable_neighbourhood_search(nr_of_iterations, objective_value, all_bookings):
    best_bookings = all_bookings
    best_costs = objective_value
    iteration = 0
    #Calculate an optimum with the current solution
    while True:
        iteration += 1
        print("Calculate local optimum")
        new_costs, new_bookings = steepest_descent(best_costs, best_bookings)
        extended_costs, extended_bookings = extended_steepest_descent(best_costs, best_bookings)
        if best_costs == new_costs:
            break
        best_bookings = new_bookings
        best_costs = new_costs

    print(best_costs)

    original_bookings = best_bookings
    best_bookings = create_backup_solution_bookings(original_bookings)
    iteration = 0
    while iteration < nr_of_iterations:
        iteration += 1
        print("Iteration ", iteration)
        temp_bookings = create_backup_solution_bookings(original_bookings)
        swap_bookings = random.sample(temp_bookings, k=2)
        # first get 2 bookings that can be swapped
        time_out_counter = 0
        while not check_swap_possibility(swap_bookings[0].rentable_id,
                                         swap_bookings[1].rentable_id,
                                         swap_bookings[0], swap_bookings[1]) and time_out_counter < 250:
            print("Checking new swap")
            time_out_counter += 1
            swap_bookings = random.sample(all_bookings, k = 2)
        if time_out_counter == 250:
            break
        # now swap
        swap_ships_in_schedule(swap_bookings[0].rentable_id,
                               swap_bookings[1].rentable_id,
                               swap_bookings[0], swap_bookings[1])

        best_cost_new_neighbor = evaluate(temp_bookings)

        while True:
            new_costs, new_bookings = steepest_descent(best_cost_new_neighbor, temp_bookings)
            if new_costs == best_cost_new_neighbor:
                # No improvement
                break
            best_cost_new_neighbor = new_costs
            temp_bookings = fill_class_dataset_with_new_data(temp_bookings, new_bookings)
        #if best compared to other minimum: update solution
        if new_costs < best_costs:
            print(new_costs)
            print(best_costs)
            best_bookings = fill_class_dataset_with_new_data(best_bookings, temp_bookings)
            best_costs = new_costs
            original_bookings = fill_class_dataset_with_new_data(original_bookings, best_bookings)
    #Return best solution and costs
    visualize(best_bookings)
    return best_costs, best_bookings