import glob

import matplotlib.pyplot as plt
import pandas as pd


def plot_data(output, xlabel, ylabel):
    print(output.to_string)



if __name__ == "__main__":
    csv_files = glob.glob('C:/Users/barry/Documents/University/CS/Minor/study tour/CR/evolve-ut/src/BookingExperts/Benchmark/*.csv')
    df_list = []
    for file in csv_files:

        df_list.append(pd.read_csv(file))

    for df in df_list:
        plot_data(df, 1, 1)
