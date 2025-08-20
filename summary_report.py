import numpy as np
import pandas as pd

class SummaryReport:
    def __init__(self, sample_list):
        self.sample_list = list(sample_list)
        self.summary_dynamic_list = [] #List needs to be dynamic due to the fixed size of dataframes

    def append_headers(self):
        self.summary_dynamic_list.append(self.sample_list)

    def find_exp_label(self, string):
        parts = string.split(": ", 1)
        if len(parts) < 2:
            raise ValueError(f"Title doesn't contain ': ': {string}")
        right_side = parts[1]  # everything after the first ": "
        return right_side

    def summary_extraction(self, processed_dataframe):
        # exp_label = processed_dataframe.find_exp_attributes()[1]
        exp_title = str(processed_dataframe.df.iloc[0, 0])
        exp_label = self.find_exp_label(exp_title)
        print(exp_label)
        row_extracted_data = [exp_label] #initialize list and append label
        sample_text_col = 1
        calcculated_avg_col = 13

        for analyte in (self.sample_list[1:]):
            found = False
            for row in range(processed_dataframe.row_size): #skip first col
                cell_value = processed_dataframe.df.iloc[row, sample_text_col]
                if isinstance(cell_value, str) and cell_value.startswith(analyte) and cell_value.endswith("A"):
                    extracted_average = processed_dataframe.df.iloc[row, calcculated_avg_col]
                    row_extracted_data.append(extracted_average)
                    found = True
                    break  # stop scanning rows once match is found
            if not found:
                row_extracted_data.append(np.nan)  # placeholder to keep dimensions square
        # print(row_extracted_data)
        self.summary_dynamic_list.append(row_extracted_data)
        # print(self.summary_dynamic_list)

    def to_dataframe(self):
        return pd.DataFrame(self.summary_dynamic_list)