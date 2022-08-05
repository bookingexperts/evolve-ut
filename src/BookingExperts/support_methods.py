# Create a set of vessels with the characteristics of the other solution
import itertools
import random
from datetime import datetime, timedelta

from data.booking import Booking
from operators import check_swap_possibility, swap_ships_in_schedule


# Open a file, and read its content according to the format.txt formatting. Return all contents at the end.
# def read_file(name):
#     file = open(name, "r")
#     lines = file.read().splitlines()
#     number_bookings = int(lines[0])
#     number_rentables = int(lines[1])
#     start_times_vessels = [int(item) for item in lines[2].split(" ") if item != ""]
#     end_time_vessels = [int(item) for item in lines[5 + number_vessels].split(" ") if item != ""]
#     opening_times_berths = [int(item) for item in lines[3].split(" ") if item != ""]
#     closing_times_berths = [int(item) for item in lines[4 + number_vessels].split(" ") if item != ""]
#     handling_times = []
#     for line in lines[4: 4 + number_vessels]:
#         list_per_vessel = line.split(" ")
#         handling_times.append([int(item) for item in list_per_vessel if item != ""])
#     handling_costs_berths = [float(item) for item in lines[6 + number_vessels].split(" ") if item != ""]
#
#     return number_vessels, number_berths, start_times_vessels, end_time_vessels, opening_times_berths, \
#         closing_times_berths, handling_times, handling_costs_berths


def read_file(name):
    file = open(name, "r")
    lines = file.read().splitlines()
    number_bookings = int(lines[0])
    number_rentables = int(lines[1])
    start_dates_bookings = [int(item) for item in lines[2].split(" ") if item != ""]
    end_dates_bookings = [int(item) for item in lines[3].split(" ") if item != ""]
    opening_dates_rentables = [int(item) for item in lines[4].split(" ") if item != ""]
    closing_dates_rentables = [int(item) for item in lines[5].split(" ") if item != ""]

    return number_bookings, number_rentables, start_dates_bookings, end_dates_bookings, opening_dates_rentables, \
        closing_dates_rentables


def read_file_with_uniform_distributions(name):
    file = open(name, "r")
    lines = file.read().splitlines()
    number_vessels = int(lines[0])
    number_berths = int(lines[1])
    start_times_vessels = [int(item) for item in lines[2].split(" ") if item != ""]
    end_time_vessels = [int(item) for item in lines[5 + number_vessels].split(" ") if item != ""]
    opening_times_berths = [int(item) for item in lines[3].split(" ") if item != ""]
    closing_times_berths = [int(item) for item in lines[4 + number_vessels].split(" ") if item != ""]
    handling_times = []
    for line in lines[4: 4 + number_vessels]:
        list_per_vessel = line.split(" ")
        handling_times.append([int(item) for item in list_per_vessel if item != ""])
    handling_costs_berths = [float(item) for item in lines[6 + number_vessels].split(" ") if item != ""]

    # Add a uniform distribution to the start times and the handling times
    start_times_vessels = [start_time + round(random.uniform(2, 5)) for start_time in start_times_vessels]
    for i, handling_time in enumerate(handling_times):
        handling_times[i] = [time + round(random.uniform(1, 7)) for time in handling_time]
    return number_vessels, number_berths, start_times_vessels, end_time_vessels, opening_times_berths, \
        closing_times_berths, handling_times, handling_costs_berths


def create_backup_solution_bookings(set_of_bookings):
    copy_of_bookings = []
    for booking in set_of_bookings:
        booking_backup = Booking(booking.id, booking.start_date, booking.end_date, booking.rentable_type)
        booking_backup.length = booking.length
        booking_backup.rentable = booking.rentable
        booking_backup.fixed = booking.fixed
        copy_of_bookings.append(booking_backup)
    return copy_of_bookings



# Create a set of berths with the characteristics of the other solution
# def create_backup_solution_berths(set_of_berths):
#     copy_of_berths = []
#     for berth in set_of_berths:
#         berth_backup = Berth(berth.opening_time, berth.closing_time, len(set_of_berths))
#         berth_backup.id = berth.id
#         berth_backup.schedule = berth.schedule
#         copy_of_berths.append(berth_backup)
#     return copy_of_berths


def fill_class_dataset_with_new_data(old_class_set, new_class_set):
    for item in range(len(old_class_set)):
        old_class_set[item].id = new_class_set[item].id
        old_class_set[item].start_date = new_class_set[item].start_date
        old_class_set[item].end_date = new_class_set[item].end_date
        old_class_set[item].length = new_class_set[item].length
        old_class_set[item].rentable = new_class_set[item].rentable
        old_class_set[item].rentable_type = new_class_set[item].rentable_type
        old_class_set[item].fixed = new_class_set[item].fixed
    return old_class_set


# Computes a list of all neighbouring solutions where two vessels are swapped
# In order to reduce complexity, a random selection of 100 neighbours is returned.
# def get_all_neighbours(vessels):
#     neighbours = []
#     # Loop over all combinations of vessels
#     for from_vessel, to_vessel in list(itertools.product(vessels, vessels)):
#         if from_vessel == to_vessel:
#             continue
#         # Check whether you can swap the two vessels.
#         if check_swap_possibility(from_vessel.helped_by_berth, to_vessel.helped_by_berth, from_vessel, to_vessel):
#             temp_vessels = create_backup_solution_vessels(vessels)
#             for temp_vessel in temp_vessels:
#                 if temp_vessel.id == from_vessel.id:
#                     from_vessel = temp_vessel
#                 if temp_vessel.id == to_vessel.id:
#                     to_vessel = temp_vessel
#             # Swap the two vessels and append the newly created solution to the neighbours list.
#             swap_ships_in_schedule(from_vessel.helped_by_berth, to_vessel.helped_by_berth, from_vessel, to_vessel)
#             neighbours.append(temp_vessels)
#     # Return 100 neighbours
#     return random.sample(neighbours, k=100)

# Computes a list of all neighbouring solutions where two vessels are swapped

def get_all_neighbours(bookings):
    neighbours = []
    # Loop over the combinations of bookings
    for from_booking, to_booking in list(itertools.product(bookings, bookings)):
        # Remove combinations with itself
        if from_booking == to_booking:
            continue
        # Check whether swap between bookings is possible
        if check_swap_possibility(from_booking.housed_by, to_booking.housed_by, from_booking, to_booking):
            temp_bookings = create_backup_solution_bookings(bookings)
            for temp_booking in temp_bookings:
                if temp_booking.id == from_booking.id:
                    from_booking = temp_booking
                if temp_booking.id == to_booking.id:
                    to_booking = temp_booking
            # Swap
            swap_ships_in_schedule(from_booking.housed_by, to_booking.housed_by)
            neighbours.append(temp_bookings)
    # Return 100 neighbours
    return random.sample(neighbours, k=100)




def kick_berths_at_index(i, j, nr_vessels, nr_berths, vessel_arriving_time, vessel_end_time, berth_opening_time,
                         berth_closing_time, handling_time, handling_costs):
    nr_berths -= 2
    berth_opening_time.pop(j)
    berth_opening_time.pop(i)
    berth_closing_time.pop(j)
    berth_closing_time.pop(i)
    for berth_times in handling_time:
        berth_times.pop(j)
        berth_times.pop(i)
    return nr_vessels, nr_berths, vessel_arriving_time, vessel_end_time, berth_opening_time, berth_closing_time, \
        handling_time, handling_costs


