import booking_utils as bu
import numpy as np

grouped_scheme = bu.generate_grouped_bookings()

print(grouped_scheme)


grouped_scheme.sort(key=lambda tup: tup[0])
for group in grouped_scheme:
    print(group)



def assign_room(bookings):
    planning = [[], [], [], [], []]
    print(planning)
    for group in bookings:
        r = 0
        while True:
            if (len(planning[r]) < 1) or (group[0][0] > planning[r][-1][0]):
                planning[r].extend(group)
                break
            r += 1
    return planning



new_scheme = assign_room(grouped_scheme)

for room in new_scheme:
  #  print(room, len(room))
    bu.show_bookings(room)



