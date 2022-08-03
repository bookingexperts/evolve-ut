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

    return all_bookings


def show_bookings(grouped_bookings):
    line_1 = ""
    line_2 = ""

    for i in range(40):
        first_digit = i // 10
        second_digit = i % 10

        line_1 += " " if first_digit == 0 else str(first_digit)
        line_2 += str(second_digit)

    print(line_1)
    print(line_2)

    for bookings in grouped_bookings:
        line = ""
        index = 0

        x = 0

        try:
            j = bookings[-1][1]
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
                    else:
                        line += "]"

                x += 1

            print(line)
        except IndexError:
            print("No bookings for this room")


def group_bookings(bookings):
    """Groups bookings where start date and end dates are the same"""
    result = []

    for booking in bookings:
        result.append([booking])

    i = 0
    while i < len(result):
        j = i + 1
        while j < len(result):
            if result[i][-1][1] == result[j][0][0]:
                result[i].extend(result[j])
                result.pop(j)
                j -= 1
            elif result[j][-1][1] == result[i][0][0]:
                result[j].extend(result[i])
                result.pop(i)
                i -= 1
                break
            j += 1
        i += 1

    return result


def better_group_bookings(bookings: List):
    bookings = bookings.copy()
    bookings.sort(key=lambda tup: tup[0])
    result = []

    i = 0
    while len(bookings) > 0:
        lengths = [end - begin for (begin, end) in bookings]
        previous_end = bookings[0][1]
        previous_index = 0
        for i in range(1, len(bookings)):
            sublengths = [0] * i
            indices = [-1] * i
            for k in range(i):
                if bookings[k][0] == previous_end:
                    sublengths[k] = lengths[k]
                    indices[k] = previous_index
            lengths[i] += max(sublengths)


def ungroup_bookings(grouped_bookings):
    result = []

    for bookings in grouped_bookings:
        result.extend(bookings)

    return result


def generate_grouped_bookings():
    bookings_per_room = generate_bookings()
    bookings = ungroup_bookings(bookings_per_room)
    return group_bookings(bookings)


def main():
    bookings_per_room = generate_bookings()
    for bookings in bookings_per_room:
        print(bookings, len(bookings))

    print()
    show_bookings(bookings_per_room)

    print()
    ungrouped_bookings = ungroup_bookings(bookings_per_room)

    grouped_bookings = group_bookings(ungrouped_bookings)

    for bookings in grouped_bookings:
        print(bookings, len(bookings))


if __name__ == '__main__':
    main()
