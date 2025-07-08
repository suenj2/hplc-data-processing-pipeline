import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

df = pd.read_excel("input.xlsx", header=None)
# df = pd.read_excel("input.xlsx", header=6, usecols="B:K")
# parse = df.parse()

# print(df.head())

# print(df.iloc[:20, :10])

for i in range(10):
    for j in range(10):
        val = df.iloc[i, j]
        if pd.notna(val):
            print(f"[{i}:{j}] -> {repr(val)}")

# xlsx format is fucked need to write a function with a for loop to find cell A1
# Will also need a global var for these

def hello_world():
    print ("Hello World")