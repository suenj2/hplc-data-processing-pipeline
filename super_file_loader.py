import pandas as pd
import os

class SuperFileLoader:
    def __init__(self, file_path, sheet_name=None):
        self.df = None
        self.num_rows = None
        self.num_cols = None

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".csv":
            self.df = pd.read_csv(file_path, header=None, dtype=object)
        # elif ext in (".xls", ".xlsx"):
        #     self.df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        elif ext in (".xls", ".xlsx"):
            if sheet_name is None:
                sheet_name = 0 #Load first sheet by default
            self.df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, dtype=object)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        self.num_rows, self.num_cols = self.df.shape

    def __str__(self):
        return f"{self.__class__.__name__} holding DataFrame:\n{self.df.to_string(index=False)}"

    def read_file_meta_data(self):
        print(f"File contains {self.num_rows} rows and {self.num_cols} columns.\n")
