import pandas as pd
import os

class FileWriter:
    @staticmethod
    def write_df_to_excel(df, filepath, sheet_name, start_row=0, start_col=0):
        # Check if the file already exists
        file_exists = os.path.exists(filepath)

        # Choose mode depending on existence
        mode = "a" if file_exists else "w"

        with pd.ExcelWriter(
            filepath,
            engine="openpyxl",
            mode=mode,
            if_sheet_exists="overlay" if file_exists else None  # only valid in append mode
        ) as writer:
            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
                header=False,
                startrow=start_row,
                startcol=start_col
            )
