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

    # static????
    def append_std_conc(self, HPLC_file_path, conc_file_path, exp_num):
        #splice concentrations from conc_file
        col_offset = -1
        # df_conc =
        #append to output file

        return False

    def pre_format(self):
        for rows in range(self.row_size):
            for cols in range(7, self.col_size):
                self.df.iloc[rows, cols] = np.nan

        self.df.iloc[1, 8] = "LINEST"
        self.df.iloc[2, 7] = "ratio"

    def ratio_calc(self):
        for row in range(3, self.row_size):
            if not pd.isna(self.df.iloc[row, 4]):
                result = float(self.df.iloc[row, 4])/float(self.df.iloc[row, 5]) #Area/IS Area
                self.df.iloc[row, 7] = result

    def conc_vial_calc(self):
        return False

    def corr_conc_calc(self):
        return False

    def conc_soil_calc(self):
        return False

    def find_exp_attributes(str):
        #split by ":"
        split_colon = str.split(":", 1)
        left = split_colon[0]
        right = split_colon[1]

        #extract experiment number from the left
        exp_num = left.split(" ")[1]

        #split right by space
        right_parts = right.split()

        #check for suffix number
        if right_parts[-1].isdigit():
            compound_name = " ".join(right_parts[:-1])
        else:
            compound_name = " ".join(right_parts)

        return exp_num, compound_name


# Test:
# print(DataProcessor.find_exp_attributes("Compound 4:  PFEtS"))
# print(DataProcessor.find_exp_attributes("Compound 4:  PFEtS 11"))
# print(DataProcessor.find_exp_attributes("Compound 9:  3:3 FTCA 12"))
# print(DataProcessor.find_exp_attributes("Compound 99: TFA 100"))


