from evaluation_booking import evaluate
from schedule_obtain import first_come_first_serve
from support_methods import get_all_neighbours


def pareto_search(name):
    counter = 0
    print("Get first random solution")
    pseudo_berths, best_vessels = first_come_first_serve(name)
    best_costs = evaluate(best_vessels)
    print("Perform swaps until the best solution is found in terms of costs")
    print("The best solution is:")
    print("Costs: ", best_costs)
    print("Get all neighbours")
    pareto_solutions = [best_vessels]
    print("Check all neighbours to see which are in the pareto set.")
    neighbours = get_all_neighbours(best_vessels)
    while counter < len(pareto_solutions):
        for solution in neighbours:
            if solution in pareto_solutions:
                continue
            solution_costs = evaluate(solution)
            if solution_costs < best_costs:
                pareto_solutions.append(solution)
                neighbours.extend(get_all_neighbours(solution))
            if len(neighbours) > 1000:
                break
        print(len(pareto_solutions), " solutions found")
        print("Countertje ", counter)
        counter += 1
    return pareto_solutions

def pareto_search_bookings(name):
    name = None