#Import libraries
import shutil
import pandas as pd

#Import classes
import data_processor
import file_reader

def filename_output(str_input):
    return str_input + "_processed"

def file_copy(src, dst):
    shutil.copy(src, dst)
    print(f"File successfully copied from {src} to {dst}")

if __name__ == '__main__':
    # Step 1: Make secure copy in output folder
    input_filename = "input" #hardcoded for now
    output_filename = filename_output(input_filename)
    file_copy(f"input/{input_filename}.xlsx", f"output/{output_filename}.xlsx")

    # Step 2: Open and process .xlsx file in output folder
    sheet_name_input = "PFAS Kitcholm soils 3,4" #hardcoded for now
    reader = file_reader.FileReader(f"output/{output_filename}.xlsx", sheet_name=f"{sheet_name_input}")
    reader.read_file_meta_data()

    # Step 3: Select the experiment number to process results
    experiment_num = 3 #hardcoded for now
    df_chunk = reader.extract_df(experiment_num)
    processing_chunk = data_processor.DataProcessor(df_chunk) #convert to data_processor object
    # print(processing_chunk)

    # Step 4: Processing of data frame
    processing_chunk.pre_format()
    processing_chunk.ratio_calc()
    processing_chunk.find_first_run()
    print(processing_chunk)
