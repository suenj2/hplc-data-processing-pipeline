import file_reader
import shutil

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
    sheetname = "PFAS Kitcholm soils 3,4" #hardcoded for now
    reader = file_reader.FileReader(f"output/{output_filename}.xlsx", sheet_name=f"{sheetname}")
    reader.read_file_meta_data()


