import itertools
from datetime import datetime, timedelta

from operators import daterange
import src.BookingExperts.data.server_communication as comm
from src.booking_utils import fill_rentable_plannings
import networkx as nx
import matplotlib.pyplot as plt


def daterange(start_date: datetime, end_date: datetime):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def evaluate(planning):
    rentables = {}
    for booking in planning:
        rentables[booking.rentable.rentable_id] = booking.rentable
    total_gaps = 0
    biggest_gap = timedelta()
    for rentable in rentables.values():
        added_gaps, potential_biggest_gap = evaluate_rentable(rentable)
        total_gaps += added_gaps
        biggest_gap = max(biggest_gap, potential_biggest_gap)
    return total_gaps, biggest_gap


def evaluate_rentable(rentable):
    schedule = [date for date in sorted(rentable.schedule.keys()) if rentable.schedule[date] is not None]
    total_gaps = 0
    biggest_gap = timedelta()

    for i in range(1, len(schedule)):
        gap_size = schedule[i] - schedule[i - 1] - timedelta(days=1)

        if gap_size >= timedelta(days=1):
            total_gaps += 1
            biggest_gap = max(biggest_gap, gap_size)

    return total_gaps, biggest_gap


# Print the evaluation of a solution.
def visualize(solution):
    total_gaps = evaluate(solution)

    print("Total number of bookings: ", len(solution))
    print("Total gaps: ", total_gaps)

    rentables = {}
    for booking in solution:
        rentables[booking.rentable.rentable_id] = booking.rentable
    rentables = sorted(rentables.values(), key=lambda rentable: rentable.rentable_id)
    # for rentable in rentables:
    #     print("Schedule Rentable ", rentable.rentable_id, ": \t", rentable.schedule)

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
                if rentable.schedule[date].fixed:
                    visual += "FFFFFFFFFF"
                else:
                    visual += "XXXXXXXXXX"

                if rentable.schedule[date].end_date - date <= timedelta(days=1):
                    visual += "|"
                else:
                    visual += " "

            else:
                visual += "           "
        visual += "\n"
    print(visual)


def visualize_original_graph(bookings):
    network = nx.Graph()
    network.add_nodes_from(bookings)
    for booking1, booking2 in itertools.combinations(bookings, 2):
        if booking1.start_date <= booking2.start_date < booking1.end_date or booking2.start_date <= booking1.start_date < booking2.end_date:
            network.add_edge(booking1, booking2)
    fig = plt.figure(figsize=(30, 30))
    nx.draw_networkx(network, with_labels=False)
    plt.show()


if __name__ == '__main__':
    print('getting bookings')
    category = comm.get_rentable_types()[0]
    bookings = comm.filter_bookings_on_type(category)
    fill_rentable_plannings(bookings)
    print('evaluating bookings')
    print(evaluate(bookings))
