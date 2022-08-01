import numpy as np

planning = np.random.randint(2, size=(5, 14))
print(planning)


def count_gaps(planning):
    count = 0
    for x in planning:
        start_count = count
        if x[0] == 0:
            count += 1
        for y in range(1, len(x)):
            count += (1 - x[y]) * x[y - 1]
    print(count)

def count_gaps_wothout_borders(planning):
    count = 0

    for row in planning:
        row_count = 0



if __name__ == '__main__':
    count_gaps(planning)
