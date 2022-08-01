import random
from typing import List

rooms = 5

def generate_bookings():
    all_bookings = []
    for i in range(rooms):
        j = 0
        bookings = []
        while j < 30:
            k = j + 5

            start_date = random.randint(j, k)
            end_date = random.randint(start_date + 1, start_date + 5)
            bookings.append((start_date, end_date))

            j = end_date
        all_bookings.append(bookings)

    # for bookings in all_bookings:
    #     print(bookings)

    return all_bookings


def show_bookings(bookings):
    line = ""
    index = 0

    # print(bookings)

    x = 0
    j = bookings[len(bookings) - 1][1]
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
            elif booking[1] == bookings[index][0]:
                line += "|"
                x += 1
            else:
                line += "]"

        x += 1

    print(line)


def group_bookings(bookings):
    """Groups bookings where start date and end dates are the same"""
    result = []

    for booking in bookings:
        result.append([booking])

    i = 0
    while i < len(result):
        j = i + 1
        while j < len(result):
            if result[i][len(result[i]) - 1][1] == result[j][0][0]:
                result[i].extend(result[j])
                result.pop(j)
                j -= 1
            elif result[j][len(result[j]) - 1][1] == result[i][0][0]:
                result[j].extend(result[i])
                result.pop(i)
                break
            j += 1
        i += 1

    return result


if __name__ == '__main__':
    all_bookings = generate_bookings()
    for bookings in all_bookings:
        print(bookings, len(bookings))

    for bookings in all_bookings:
        show_bookings(bookings)

    ungrouped_bookings = []
    for bookings in all_bookings:
        ungrouped_bookings.extend(bookings)

    grouped_bookings = group_bookings(ungrouped_bookings)

    for bookings in grouped_bookings:
        print(bookings, len(bookings))
