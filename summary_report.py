class SummaryReport:
    def __init__(self, sample_list):
        self.sample_list = list(sample_list)
        self.summary_dynamic_list = [] #List needs to be dynamic due to the fixed size of dataframes

    def append_headers(self):
        self.summary_dynamic_list.append(self.sample_list)

    def summary_extraction(self, processed_dataframe):
        #Need for loop to iterate over the titles checking for prefix and suffix
        #When the conditional is met, look to the right and extract summary data
        return False