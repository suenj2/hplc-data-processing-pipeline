import HPLC_file_loader
import pandas as pd
import numpy as np
import scipy.stats as stats

class DataProcessor:
    def __init__(self, df_chunk):
        self.df = df_chunk
        self.exp_num, self.compound_name = self.find_exp_attributes()
        self.starting_coordinate = (df_chunk.index.min(), int(df_chunk.columns.min()))
        self.row_size, self.col_size = df_chunk.shape
        self.row_first_run = None

        try:
            self.row_first_run = self.find_first_run()
            print(f"Dataframe successfully loaded:")
            print(f"Experiment: {self.exp_num}")
            print(f"Compound: {self.compound_name}\n")
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

    def find_exp_attributes(self):
        exp_title = self.df.iloc[0, 0]

        #split by ":"
        split_colon = exp_title.split(":", 1)
        left = split_colon[0]
        right = split_colon[1]

        #extract experiment number from the left
        exp_num = int(left.split(" ")[1])

        #split right by space
        right_parts = right.split()

        #check for suffix number
        if right_parts[-1].isdigit():
            compound_name = " ".join(right_parts[:-1])
        else:
            compound_name = " ".join(right_parts)

        return exp_num, compound_name

    def append_std_conc(self, dict):
        exp_num, compound_name = self.find_exp_attributes()
        sub_conc_df = dict[compound_name]

        start_row, start_col = 3, 2  # origin cell for insertion
        end_row = start_row + sub_conc_df.shape[0]
        end_col = start_col + sub_conc_df.shape[1]

        self.df.iloc[start_row:end_row, start_col:end_col] = sub_conc_df.values

        return self.df

    def pre_format(self):
        for rows in range(self.row_size):
            for cols in range(7, self.col_size):
                self.df.iloc[rows, cols] = np.nan

        self.df.iloc[2, 7] = "ratio"

    def ratio_calc(self):
        for row in range(3, self.row_size):
            if not pd.isna(self.df.iloc[row, 4]):
                result = float(self.df.iloc[row, 4])/float(self.df.iloc[row, 5]) #Area/IS Area
                self.df.iloc[row, 7] = result

    def linest(self):
        x = np.array(self.df.iloc[6:11, 2].tolist(), dtype=float)
        y = np.array(self.df.iloc[6:11, 7].tolist(), dtype=float)
        n = len(x)

        # Regression analysis
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        y_predicted = slope * x + intercept
        residuals = y - y_predicted

        # Deg of freedom
        deg_freedom = n - 2

        # Sum of squares
        ss_total = np.sum((y - np.mean(y)) ** 2)
        ss_res = np.sum(residuals ** 2)
        ss_reg = ss_total - ss_res

        # SEE (Standard error of y estimate)
        see = np.sqrt(ss_res / deg_freedom)

        # Manual Std Error of Intercept
        denominator = np.sum((x - np.mean(x)) ** 2)
        se_intercept = (
            see * np.sqrt(np.sum(x ** 2) / (n * denominator)) if denominator != 0 else np.nan
        )

        # F-statistic
        ms_reg = ss_reg / 1
        ms_res = ss_res / deg_freedom
        f_stat = ms_reg / ms_res

        # Create dataframe
        output = np.array([
            [slope, intercept],
            [std_err, se_intercept],
            [r_value ** 2, see],
            [f_stat, deg_freedom],
            [ss_reg, ss_res]
        ])
        linest_df = pd.DataFrame(
            output,
            index=["slope/intercept", "stderr", "R2/SEE", "F/df", "SSR/SSE"],
            columns=["Col1 (slope)", "Col2 (intercept)"]
        )

        # Append to self data frame
        self.df.iloc[1, 8] = "LINEST" #print title
        start_row, start_col = 2, 8  # origin cell for insertion
        end_row = start_row + linest_df.shape[0]
        end_col = start_col + linest_df.shape[1]

        self.df.iloc[start_row:end_row, start_col:end_col] = linest_df.values

        return linest_df

    def conc_vial_calc(self):
        return False

    def corr_conc_calc(self):
        return False

    def conc_soil_calc(self):
        return False

# Test:
# print(DataProcessor.find_exp_attributes("Compound 4:  PFEtS"))
# print(DataProcessor.find_exp_attributes("Compound 4:  PFEtS 11"))
# print(DataProcessor.find_exp_attributes("Compound 9:  3:3 FTCA 12"))
# print(DataProcessor.find_exp_attributes("Compound 99: TFA 100"))


