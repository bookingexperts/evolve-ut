from datetime import datetime, timedelta
from operators import daterange


def evaluate(planning):
    rentables = set([booking.rentable_id for booking in planning])
    print(rentables)
    total_gaps = 0
    current_date = datetime.strptime('2022-05-16', '%Y-%m-%d')
    for rentable in rentables:
        print(rentable.schedule)
        schedule = sorted(rentable.schedule.keys())
        for date in daterange(schedule[0], schedule[-1]):
            if date in rentable.schedule.keys() and date - timedelta(days=1) not in rentable.schedule.keys():
                total_gaps += 1
        if schedule[-1] is None:
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
    return total_berth_handling, total_berth_handling + total_berth_slots_empty,


# Print the evaluation of a solution.
def visualize(solution):
    total_gaps = evaluate(solution)

    print("Total number of bookings: ", len(solution))
    print("Total gaps: ", total_gaps)
    rentables = set([booking.rentable_id for booking in solution])
    for rentable in rentables:
        print("Schedule Rentable ", rentable.id, ": \t", rentable.schedule)

    current_date = datetime.strptime('2022-05-16', '%Y-%m-%d')
    last_date = current_date

    visual = "Schedule:\n"
    for rentable in rentables:
        last_local = sorted(rentable.schedule.keys())[-1]
        if last_local > last_date:
            last_date = last_local
    last_date += timedelta(days=1)
    visual += "Day: "
    for date in daterange(current_date, last_date):
        visual += date.strftime("%Y-%m-%d") + " "
    visual += "\n"
    for rentable in rentables:
        visual += "     "
        for date in daterange(current_date, last_date):
            if date in rentable.schedule.keys():
                visual += "XXXXXXXXXX "
            else:
                visual += "           "
        visual += "\n"
    print(visual)
