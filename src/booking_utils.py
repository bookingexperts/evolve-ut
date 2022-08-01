import random

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


def show_bookings(bookings):
    line = ""
    index = 0

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

    line_1 = ""
    line_2 = ""

    for i in range(40):
        first_digit = i // 10
        second_digit = i % 10
        line_1 += " " if first_digit == 0 else str(first_digit)
        line_2 += str(second_digit)
    print(line_1)
    print(line_2)

    for bookings in bookings_per_room:
        show_bookings(bookings)

    print()
    ungrouped_bookings = ungroup_bookings(bookings_per_room)

    grouped_bookings = group_bookings(ungrouped_bookings)

    for bookings in grouped_bookings:
        print(bookings, len(bookings))


if __name__ == '__main__':
    main()
