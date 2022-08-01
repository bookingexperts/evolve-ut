import random

all_bookings = []
for i in range(5):
    j = 0
    bookings = []
    while j < 30:
        k = j + 5

        start_date = random.randint(j, k)
        end_date = random.randint(start_date + 1, start_date + 5)
        bookings.append((start_date, end_date))

        j = end_date
    all_bookings.append(bookings)

    line = ""
    index = 0

    # print(bookings)

    x = 0
    while x <= j:
        booking = bookings[index]

        if x < booking[0]:
            line += " "
        elif x == booking[0]:
            line += "["
        elif booking[0] < x < booking[1]:
            line += "="
        elif x == booking[1]:
            index += 1

            if index == len(bookings):
                line += "]"
                break
            elif booking[1] != bookings[index][0]:
                line += "]"
            else:
                line += "|"
                x += 1

        x += 1

    print(line)

for bookings in all_bookings:
    print(bookings)
