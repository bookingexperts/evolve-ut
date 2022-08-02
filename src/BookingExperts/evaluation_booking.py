# def evaluate(vessels):
#     total_waiting_time = 0.0
#     total_costs = 0.0
#     for vessel in vessels:
#         total_waiting_time += vessel.time_accepted - vessel.arrival_time
#         total_costs += float(vessel.time_left - vessel.arrival_time) * float(vessel.handling_costs)
#     return round(total_costs, 2)

def evaluate(planning):
    total_gaps = 0
    for rentable in planning:
        if rentable.schedule[0] == "":
            total_gaps += 1
        for day in range(1, len(rentable.schedule)):
            if rentable.schedule[day] == "" and rentable.schedule[day-1] != "":
                total_gaps += 1
        if rentable.schedule[-1] == "":
            total_gaps -= 1
    return total_gaps


def compute_utilization(solution):
    berths = set([vessel.helped_by_berth for vessel in solution])
    total_berth_slots_empty = 0
    total_berth_handling = 0
    for berth in berths:
        for i in range(len(berth.schedule)):
            if berth.schedule[i] == "":
                total_berth_slots_empty += 1
            elif berth.schedule[i] != "XX":
                total_berth_handling += 1
    return total_berth_handling, total_berth_handling+total_berth_slots_empty,


# Print the evaluation of a solution.
def visualize(solution):
    total_gaps = 0
    for x in solution:
        if x[0] == 0:
            total_gaps += 1
        for y in range(1, len(x)):
            total_gaps += (1 - x[y]) * x[y - 1]
    print(solution)
    # print("Total number of vessels: ", len(solution))
    # print("Total waiting time: ", total_waiting_time)
    # print("Total costs: €", round(total_costs, 2))
    # berths = set([vessel.helped_by_berth for vessel in solution])
    # total_berth_slots_empty = 0
    # total_berth_handling = 0
    # for berth in berths:
    #     for i in range(len(berth.schedule)):
    #         if berth.schedule[i] == "":
    #             berth.schedule[i] = "  "
    #             total_berth_slots_empty += 1
    #         elif berth.schedule[i] != "XX":
    #             total_berth_handling += 1
    #     print("Schedule berth ", berth.id, ": \t", berth.schedule)
    # print("Total utilization: ", total_berth_handling, total_berth_slots_empty+total_berth_handling, round(total_berth_handling /
    #       (total_berth_slots_empty + total_berth_handling), 3))


# Returns the latest end time of a vessel in a solution
def calculate_makespan(vessels):
    end_time = -1
    for vessel in vessels:
        if vessel.time_left > end_time:
            end_time = vessel.time_left
    return end_time
