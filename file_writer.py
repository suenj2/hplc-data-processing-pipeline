import pandas as pd
import os

class FileWriter:
    # @staticmethod
    # def write_df_to_excel(df, filepath, sheet_name, start_row, start_col):
    #     with pd.ExcelWriter(
    #         filepath,
    #         engine="openpyxl",
    #         mode="a", #append mode. Does not overwrite the entire sheet
    #         if_sheet_exists="overlay"
    #     ) as writer:
    #         df.to_excel(
    #             writer,
    #             sheet_name=sheet_name,
    #             index=False, #do not add left row indices
    #             header=False, #do not add top col headers
    #             startrow=start_row,
    #             startcol=start_col
    #         )

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

# df_test = pd.DataFrame({
#     "Column 1": [1, 2, 3],
#     "Column 2": ["A", "B", "C"]
# })
# FileWriter.write_df_to_excel(df_test, "output/input_processed.xlsx", "PFAS Kitcholm soils 3,4", 0, 0)
