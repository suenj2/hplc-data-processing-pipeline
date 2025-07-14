import HPLC_file_loader
import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, df_chunk):
        self.df = df_chunk
        self.starting_coordinate = (df_chunk.index.min(), int(df_chunk.columns.min()))
        self.row_size, self.col_size = df_chunk.shape
        self.row_first_run = None

        # print(self.starting_coordinate)
        # print(self.row_size)
        # print(self.col_size)

        try:
            self.row_first_run = self.find_first_run()
        except ValueError:
            print("Warning: no first run found.")

    def __str__(self):
        return f"DataProcessor holding DataFrame:\n{self.df}"

    def find_first_run(self): #returns the row of the first non-calibration run
        sample_text_col = 1
        first_exp_row = 0
        MeOH_wash_count = 0
        for row in range(2, self.row_size):
            if self.df.iloc[row, sample_text_col] == "MeOH":
                MeOH_wash_count += 1
            else:
                MeOH_wash_count = 0
            if MeOH_wash_count == 2:
                first_exp_row = row + 1
                print(f"First experiment was found at row {first_exp_row}")
                return first_exp_row
        raise ValueError(f"First run not found")

    def pre_format(self):
        for rows in range(self.row_size):
            for cols in range(7, self.col_size):
                self.df.iloc[rows, cols] = np.nan

        self.df.iloc[0, 8] = "LINEST"
        self.df.iloc[1, 7] = "ratio"

    def ratio_calc(self):
        for row in range(2, self.row_size):
            if not pd.isna(self.df.iloc[row, 4]):
                result = float(self.df.iloc[row, 4])/float(self.df.iloc[row, 5]) #Area/IS Area
                self.df.iloc[row, 7] = result

    def conc_vial_calc(self):
        return False

    def corr_conc_calc(self):
        return False

    def conc_soil_calc(self):
        return False



