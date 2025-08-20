import numpy as np

class SummaryReport:
    def __init__(self, sample_list):
        self.sample_list = list(sample_list)
        self.summary_dynamic_list = [] #List needs to be dynamic due to the fixed size of dataframes

    def append_headers(self):
        self.summary_dynamic_list.append(self.sample_list)

    def summary_extraction(self, processed_dataframe):
        #Need for loop to iterate over the titles checking for prefix and suffix
        #When the conditional is met, look to the right and extract summary data
        row_extracted_data = []
        sample_text_col = 1
        calcculated_avg_col = 13
        for analyte in self.sample_list:
            for row in range(processed_dataframe.row_size):
                cell_value = processed_dataframe.df.iloc[row, sample_text_col]
                if isinstance(cell_value, str) and cell_value.startswith(analyte) and cell_value.endswith("A"):
                    extracted_average = processed_dataframe.df.iloc[row, calcculated_avg_col]
                    print(f"{analyte}: {extracted_average}")


