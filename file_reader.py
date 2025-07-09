import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

df = pd.read_excel("input.xlsx", sheet_name="PFAS Kitcholm soils 3,4", header=None)

print(df.iloc[0,0])

def exp_num():
    return False

# for i in range(4):
#     for j in range(4):
#         val = df.iloc[i, j]
#         if pd.notna(val):
#             print(f"[{i}:{j}] -> {repr(val)}")

# xlsx format is fucked need to write a function with a for loop to find cell A1
# Will also need a global var for these