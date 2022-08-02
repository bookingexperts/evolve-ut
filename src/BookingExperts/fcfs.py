# Place the vessels at a berths using the First come first serve technique
from Assignment2.berth import Berth
from Assignment2.support_methods import read_file
from Assignment2.vessel import Vessel

def first_come_first_serve(name):
    nr_vessels, nr_berths, vessel_arriving_time, vessel_leaving_time, berth_opening_time, berth_closing_time, \
        handling_time, handling_costs = read_file(name)
    current_time = 0
    queue_for_berths = []
    vessels_in_process = []
    handled_vessels = []
    # Create a list of all vessels and berths
    all_vessels = [Vessel(vessel_arriving_time[i], vessel_leaving_time[i], handling_costs[i], handling_time[i]) for i in
                   range(0, nr_vessels)]
    all_berths = [Berth(berth_opening_time[j], berth_closing_time[j], nr_berths) for j in range(0, nr_berths)]
    last_closing_time = 0
    for j in all_berths:
        if last_closing_time < j.closing_time:
            last_closing_time = j.closing_time
    for i in all_berths:
        i.define_closing_time(last_closing_time)
    # Loop over each timestamp to see which vessels need to be served at what time.
    while len(handled_vessels) < nr_vessels:
        current_time += 1

        # Add arriving vessels to the queue
        for i in range(0, nr_vessels):
            if all_vessels[i].arrival_time == current_time:
                queue_for_berths.append(all_vessels[i])

        # Set each berths to available, if it is available
        for i in range(0, nr_berths):
            all_berths[i].update_availability(current_time)

        # If there is a queue, loop over each vessel (ship) in the queue to see if a vessel is available to handle them
        if len(queue_for_berths) > 0:
            for ship in queue_for_berths:
                for berth in all_berths:
                    if berth.check_compatibility(current_time, ship) and ship.time_accepted == 0:
                        ship.acceptance_time(current_time, berth)
                        berth.fill_schedule(ship.id, ship.handling_time[berth.id], current_time)
                        vessels_in_process.append(ship)
            queue_for_berths = [vessel for vessel in queue_for_berths if vessel.time_accepted == 0]

        # Loop over all vessels that are at a berth. If they are done, add them to the handled vessels list
        if len(vessels_in_process) > 0:
            for ship in vessels_in_process:
                if ship.check_handling_status(current_time):
                    handled_vessels.append(ship)
            vessels_in_process = [vessel for vessel in vessels_in_process if vessel.time_left == 0]
    return all_berths, all_vessels
