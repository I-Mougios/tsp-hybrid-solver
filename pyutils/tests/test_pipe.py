# In[0]: Imports
import io
import csv
import pandas as pd
from pathlib import Path
import sys
root_dir = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(root_dir))
from pyutils.decorators import trim_whitespaces, apply_to_return_value

# In[1] Create the test csv file
rows = [
        ["ID", "Name", "Age", "City", "Salary", "Department"],
        [1, "Alice   ", 30, "New York", 70000, "HR"],
        [2, "Bob", 25, "San Francisco", 80000, "Engineering"],
        [3, "  Charlie", 35, "Los Angeles ", 90000, "Finance"],
        [4, "David", 28, "Seattle", 75000, " Marketing"],
        [5, "Emma", 40, "Chicago", 85000, "Sales"],
        [6, "\tFrank", 33, "Boston", 72000, "\tEngineering "],
        [7, "Grace", 29, "Austin", 76000, "HR"],
        [8, "Henry", 45, " Denver", 88000, "Finance"],
        [9, "Isabel", 26, "Miami ", 81000, "Marketing"],
        [10, "Jack ", 38, " Dallas", 93000, "Sales"],
        [6, "\tFrank", 33, "Boston  ", 72000, "\tEngineering "],
        [8, "\tHenry", 45, " Denver  ", 88000, "   Finance"],
        ]

# Writting to an in memory file using stringIO
with io.StringIO() as buffer:
    writer = csv.writer(buffer)
    writer.writerows(rows)

    # Before close the file let's get what is insdide the buffer so we can read it with stringIO
    csv_file = buffer.getvalue()

# In[2] Define the behaviour of trim_whitespaces for dataframes and test it using the apply_to_return_value decorator

@trim_whitespaces.register
def _(serie: pd.Series) -> pd.Series:
    return serie.apply(trim_whitespaces)

@trim_whitespaces.register
def _(df: pd.DataFrame) -> pd.DataFrame:
    copy = df.copy()
    for col in copy.columns:
        # Reminder that each column is a Series object
        # and we can apply the trim_whitespaces function
        copy[col] = trim_whitespaces(copy[col])
    return copy


@apply_to_return_value(fn=trim_whitespaces)
def read_csv(*args, **kwargs):
    return pd.read_csv(*args, **kwargs)

csv_buffer = io.StringIO(csv_file)
print(read_csv(csv_buffer, sep=','))


# In[3] Stack two function using the apply_to_return_value decorator
def drop_duplicates(df: pd.DataFrame,
                    *,
                    subset: list[str], keep: str, ignore_index: bool) -> pd.DataFrame:
    copy = df.copy()
    return copy.drop_duplicates(subset=subset,
                                keep=keep,
                                ignore_index=ignore_index)

@apply_to_return_value(fn= lambda df: drop_duplicates(df,subset=df.columns,keep='first',ignore_index=True))
@apply_to_return_value(fn=trim_whitespaces)
def read_csv(*args, **kwargs):
    return pd.read_csv(*args, **kwargs)

csv_buffer = io.StringIO(csv_file)
print(read_csv(csv_buffer, sep=','))



# In[4] Using the Pipe Class
from pipe import Pipe

employees_pipe = Pipe(callables=[trim_whitespaces,
                                 lambda df: drop_duplicates(df,subset=df.columns,keep='first',ignore_index=True)],
                                 
                    debug=True)


@apply_to_return_value(fn=employees_pipe)
def read_csv(*args, **kwargs):
    return pd.read_csv(*args, **kwargs)


csv_buffer = io.StringIO(csv_file)
print(read_csv(csv_buffer, sep=','))
# %%
