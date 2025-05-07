# In[0]: Imports
from pathlib import Path
import sys
root_dir = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(root_dir))
from pyutils.decorators import apply_to_return_value


#In Demonstrating how decorator works
def remove_whitespaces(arg: str):
    print('Remove whitespaces was called')
    return arg.strip()

def upper(arg: str):
    print(f'To upper was called with arg: {arg}')
    return arg.upper()


@apply_to_return_value(fn=upper)
@apply_to_return_value(fn=remove_whitespaces) # execution for inner from bottom to top
def my_func():
    return '           Hello World  '


print(my_func())
