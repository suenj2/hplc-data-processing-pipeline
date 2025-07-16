import pandas as pd


class FileWriter:
    @staticmethod
    def write_df_to_excel(df, filepath, sheet_name, start_row, start_col):
        with pd.ExcelWriter(
            filepath,
            engine="openpyxl",
            mode="a", #append mode. Does not overwrite the entire sheet
            if_sheet_exists="overlay"
        ) as writer:
            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False, #do not add left row indices
                header=False, #do not add top col headers
                startrow=start_row,
                startcol=start_col
            )

# df_test = pd.DataFrame({
#     "Column 1": [1, 2, 3],
#     "Column 2": ["A", "B", "C"]
# })
# FileWriter.write_df_to_excel(df_test, "output/input_processed.xlsx", "PFAS Kitcholm soils 3,4", 0, 0)
