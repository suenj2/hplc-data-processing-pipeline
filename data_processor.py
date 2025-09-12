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
        self.biosolid_masses_dict = {}

        try:
            self.row_first_run = self.find_first_run()
            print(f"Dataframe successfully loaded:")
            print(f"Experiment: {self.exp_num}")
            print(f"Compound: {self.compound_name}\n")
        except ValueError:
            print("Warning: no first run found.")

    def __str__(self):
        return f"DataProcessor holding DataFrame:\n{self.df}"

    def process_all_steps(self, concentration_dict):
        self.pre_format()
        self.append_std_conc_and_spike(concentration_dict)
        self.append_biosolid_masses()
        self.ratio_calc()
        self.linest()
        self.conc_vial_calc()
        self.corr_conc_calc()
        self.conc_soil_calc()
        self.average_calc() ##!!!!!!!!BUG IN THIS METHOD CHECK IT!!!!
        # self.SD_calc()
        # self.format_combined_col()
        # self.perc_recovery_uncertainty_combined()
        # self.LOD_LOQ_calc()

    def is_exp(self):
        return pd.notna(self.df.iloc[3, 3])

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

    def append_std_conc_and_spike(self, dict):
        exp_num, compound_name = self.find_exp_attributes()
        sub_conc_df = dict[compound_name]
        row_end_conc = 0

        for row in range(sub_conc_df.shape[0]):
            if not pd.isna(sub_conc_df.iloc[row, 0]):
                row_end_conc += 1
            else:
                break

        sub_df_concs = sub_conc_df.iloc[:row_end_conc, :]
        spike_value = float(sub_conc_df.iloc[-1, 0])

        start_row, start_col = 3, 2  # origin cell for insertion

        end_row = start_row + sub_df_concs.shape[0]
        end_col = start_col + sub_df_concs.shape[1]

        self.df.iloc[start_row:end_row, start_col:end_col] = sub_df_concs.values
        self.df.iloc[9, 9] = "Spike"
        self.df.iloc[10, 9] = spike_value

        return self.df

    def set_biosolid_masses(self, biosolid_dict):
        self.biosolid_masses_dict = biosolid_dict

    def append_biosolid_masses(self):
        self.df.iloc[1, 16] = "Biosolids Masses"
        self.df.iloc[1, 17] = "(g)"

        row = 3
        for sample_id, mass in self.biosolid_masses_dict.items():
            self.df.iloc[row, 16] = sample_id
            self.df.iloc[row, 17] = mass
            row += 1

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
        self.df.iloc[11, 8] = "Conc.In Vial (ppb)"
        slope = self.df.iloc[2, 8]
        intercept = self.df.iloc[2, 9]

        if pd.isna(slope) or slope == 0:
            raise ZeroDivisionError("Slope is zero or NaN in conc_vial_calc")

        for row in range(self.row_first_run, self.row_size):
            ratio = self.df.iloc[row, 7]
            if pd.notna(ratio):
                self.df.iloc[row, 8] = (ratio - intercept) / slope

        self.df.iloc[9, 8] = "Background"
        mean = self.df.iloc[self.row_first_run:self.row_first_run+3, 8].mean()
        self.df.iloc[10, 8] = mean

    def corr_conc_calc(self):
        self.df.iloc[11, 9] = "Corr. Conc.(ppb)"

        background = self.df.iloc[10, 8]
        if background <= 0:
            background = 0

        for row in range(self.row_first_run, self.row_size):
            if not pd.isna(self.df.iloc[row, 8]):
                conc = self.df.iloc[row, 8] - background
                self.df.iloc[row, 9] = conc

    def conc_soil_calc(self):
        self.df.iloc[11, 10] = "Conc. In soil (ng/g)"

        for row in range(self.row_first_run, self.row_first_run+3):
            if not pd.isna(self.df.iloc[row, 9]):
                conc = self.df.iloc[row, 9] * 1.1
                self.df.iloc[row, 10] = conc

        biosolid_row = 3
        for row in range(self.row_first_run+3, self.row_size): #for loop range is correct calculations requires biosolid masses
            if not pd.isna(self.df.iloc[row, 9]) and (self.df.iloc[row, 1] ==  self.df.iloc[biosolid_row, 16]):
                conc = (self.df.iloc[row, 9]/self.df.iloc[biosolid_row, 17]) * 1.1
                self.df.iloc[row, 10] = conc
                biosolid_row += 1

    # def average_calc(self):
    #     row_count = 0
    #     total = 0
    #     for row in range(self.row_first_run, self.row_size):
    #         if not pd.isna(self.df.iloc[row, 10]) and row_count <= 2:
    #             total += self.df.iloc[row, 10]
    #             row_count += 1
    #         if row_count == 3:
    #             self.df.iloc[row-3, 11] = "Average"
    #             self.df.iloc[row-2, 11] = total/row_count
    #             row_count = 0
    #             total = 0
    #
    # def SD_calc(self):
    #     data = []
    #     row_count = 0
    #     for row in range(self.row_first_run, self.row_size):
    #         if not pd.isna(self.df.iloc[row, 10]) and row_count <= 2:
    #             data.append(self.df.iloc[row, 10])
    #             row_count += 1
    #         if row_count == 3:
    #             self.df.iloc[row-3, 12] = "Stdev"
    #             self.df.iloc[row-2, 12] = np.std(data, ddof=1)
    #             row_count = 0
    #             data = []
    #
    # def format_combined_col(self):
    #     for row in range(self.row_first_run, self.row_size):
    #         if pd.notna(self.df.iloc[row, 12]) and isinstance(self.df.iloc[row, 12], (int, float)):
    #             self.df.iloc[row-1, 13] = "Combined"
    #             self.df.iloc[row, 13] = f"{self.df.iloc[row, 10]:.1f} ± {self.df.iloc[row, 11]:.1f}"
    #
    # def _get_triplet_base(self, r, sample_col):
    #     """Return base name if rows r..r+2 are exactly baseA/baseB/baseC."""
    #     try:
    #         a = self.df.iloc[r, sample_col]
    #         b = self.df.iloc[r + 1, sample_col]
    #         c = self.df.iloc[r + 2, sample_col]
    #     except IndexError:
    #         return None
    #     if not (isinstance(a, str) and isinstance(b, str) and isinstance(c, str)):
    #         return None
    #     if not (a.endswith("A") and b.endswith("B") and c.endswith("C")):
    #         return None
    #     base = a[:-1]
    #     if b[:-1] != base or c[:-1] != base:
    #         return None
    #     return base
    #
    # def average_calc(self):
    #     sample_col = 1
    #     conc_col = 10
    #     avg_col = 11
    #
    #     r = self.row_first_run
    #     while r < self.row_size:
    #         base = self._get_triplet_base(r, sample_col) if hasattr(self, "_is_triplet") else self._get_triplet_base(self, r, sample_col)
    #         if base:
    #             vals = self.df.iloc[r:r + 3, conc_col].astype(float)
    #             if vals.notna().all():
    #                 # headers one row above A row; value on A row
    #                 self.df.iloc[r - 1, avg_col] = "Average"
    #                 self.df.iloc[r, avg_col] = float(vals.mean())
    #             r += 3  # jump to next block
    #         else:
    #             r += 1

    def extract_mean_from_df(self, df):
        sum = 0
        trials = 0
        for row in range(df.shape[0]):
            if pd.notna(df.iloc[row]):
                sum += df.iloc[row]
                trials += 1
        if trials != 0:
            mean = sum/trials
        else:
            mean = 0
        return (mean, trials)

    def average_calc(self):
        sample_col = 1
        conc_col = 10
        avg_col = 11
        row = self.row_first_run

        while row < self.row_size:
            cell = self.df.iloc[row, sample_col]
            if pd.notna(cell) and cell != "MeOH":
                extract_triple_df = self.df.iloc[row:row+3, conc_col]
                self.extract_mean_from_df(extract_triple_df)
                mean, trials = self.extract_mean_from_df(extract_triple_df)
                print(f"mean is {mean}")
                print(f"{trials} trials")
                row += 3
            else:
                row += 1

    def SD_calc(self):
        sample_col = 1
        conc_col = 10
        sd_col = 12

        r = self.row_first_run
        while r < self.row_size:
            base = self._get_triplet_base(r, sample_col) if hasattr(self, "_is_triplet") else self._get_triplet_base(self, r, sample_col)
            if base:
                vals = self.df.iloc[r:r + 3, conc_col].astype(float)
                if vals.notna().all():
                    self.df.iloc[r - 1, sd_col] = "Stdev"
                    self.df.iloc[r, sd_col] = float(vals.std(ddof=1))
                r += 3
            else:
                r += 1

    def format_combined_col(self):
        sample_col = 1
        avg_col = 11
        sd_col = 12
        comb_col = 13

        r = self.row_first_run
        while r < self.row_size:
            base = self._get_triplet_base(r, sample_col) if hasattr(self, "_is_triplet") else self._get_triplet_base(self, r, sample_col)
            if base:
                avg = self.df.iloc[r, avg_col]
                sd = self.df.iloc[r, sd_col]
                if pd.notna(avg) and pd.notna(sd):
                    self.df.iloc[r - 1, comb_col] = "Combined"
                    self.df.iloc[r, comb_col] = f"{float(avg):.1f} ± {float(sd):.1f}"
                r += 3
            else:
                r += 1

    def perc_recovery_uncertainty_combined(self):
        self.df.iloc[15, 13] = "%Recovery"
        self.df.iloc[15, 14] = "Uncertainty"
        self.df.iloc[15, 15] = "Combined"

        average = self.df.iloc[16 ,11]
        stdev = self.df.iloc[16 ,12]
        spike = self.df.iloc[10, 9]

        if spike and spike != 0:
            self.df.iloc[16, 13] = (average / spike) * 100
            self.df.iloc[16, 14] = (stdev / spike) * 100
            self.df.iloc[16, 15] = f"{self.df.iloc[16, 13]:.1f} ± {self.df.iloc[16, 14]:.1f}"
        else:
            self.df.iloc[16, 13] = "DIV/0"
            self.df.iloc[16, 14] = "DIV/0"

    def LOD_LOQ_calc(self):
        LOD = 0
        LOQ = 0

        if self.df.iloc[6, 6] > 3:
            LOD = self.df.iloc[6, 2]
        elif self.df.iloc[7, 6] > 3:
            LOD = self.df.iloc[7, 2]
        elif self.df.iloc[8, 6] > 3:
            LOD = self.df.iloc[8, 2]
        elif self.df.iloc[9, 6] > 3:
            LOD = self.df.iloc[9, 2]
        else:
            LOD = self.df.iloc[10, 2]

        if self.df.iloc[6, 6] > 10:
            LOQ = self.df.iloc[6, 2]
        elif self.df.iloc[7, 6] > 10:
            LOQ = self.df.iloc[7, 2]
        elif self.df.iloc[8, 6] > 10:
            LOQ = self.df.iloc[8, 2]
        elif self.df.iloc[9, 6] > 10:
            LOQ = self.df.iloc[9, 2]
        else:
            LOQ = self.df.iloc[10, 2]

        self.df.iloc[2, 11] = "By S/N Ratio"
        self.df.iloc[3, 10] = "LOD"
        self.df.iloc[4, 10] = "LOQ"
        self.df.iloc[3, 11] = LOD
        self.df.iloc[4, 11] = LOQ

    def write_chunk_to_df(self, main_df):
        start_row, start_col = self.starting_coordinate
        main_df.iloc[start_row:start_row + self.row_size, start_col:start_col + self.col_size] = self.df.values

# Test:
# print(DataProcessor.find_exp_attributes("Compound 4:  PFEtS"))
# print(DataProcessor.find_exp_attributes("Compound 4:  PFEtS 11"))
# print(DataProcessor.find_exp_attributes("Compound 9:  3:3 FTCA 12"))
# print(DataProcessor.find_exp_attributes("Compound 99: TFA 100"))


