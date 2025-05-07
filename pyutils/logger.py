# loggers.py
from pathlib import Path
import sys
import logging
from typing import Callable, Any
from functools import wraps
from datetime import datetime

__all__ = ['logger', 'log']

# Dynamically determine the log path
log_directory = Path(__file__).parents[1] / 'logs'
log_directory.mkdir(parents=True, exist_ok=True)

log_path = str(log_directory.joinpath(f"{datetime.now().strftime('%Y-%m-%dT%H_%M_%S')}.log"))


# Create the logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create the console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(module)s - %(message)s')
console_handler.setFormatter(console_formatter)

# File handler for warnings and above
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def log(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that logs the execution of a function, including its arguments and any exception raised.

    Parameters:
    fn (Callable[..., Any]): The function to be decorated.

    Returns:
    Callable[..., Any]: The wrapped function that logs its execution details.
    """
    @wraps(fn)
    def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        """
        Wrapper function that logs the function's name, arguments, and exceptions (if any).

        Parameters:
        *args (tuple[Any, ...]): Positional arguments passed to the decorated function.
        **kwargs (dict[str, Any]): Keyword arguments passed to the decorated function.

        Returns:
        Any: The result of the decorated function `fn`.

        Raises:
        Exception: Re-raises any exception raised by `fn` after logging it.
        """
        # Convert positional arguments to strings and join them with commas
        args_str = ', '.join(map(str, args)) if args else ""

        # Convert keyword arguments to "key=value" format and join with commas
        kwargs_str = ', '.join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""

        # Build a formatted debug message showing the function name and its arguments
        logger.debug(
            f'Executing {fn.__name__}({args_str}{", " if args_str and kwargs_str else ""}{kwargs_str})...'
        )

        try:
            # Call the original function with all arguments
            result = fn(*args, **kwargs)
            return result
        except Exception as e:
            # Log the exception with a message indicating the function where it occurred
            logger.exception(f"Fail to execute the function {fn.__name__}: {e}")
            # Re-raise the exception to maintain normal error propagation
            raise e

    return wrapper


if __name__ == '__main__':
    import numpy as np
    import pandas as pd

    @log
    def open_file(*args, **kwargs):
        pass

    @log
    def raise_error():
        raise ValueError('This is a custom error message')


    with open(log_path, 'a') as f:
        f.write("==== Start of New Execution ====\n")

    open_file(1, 2, 3, filename='file1.txt', a=1, b=2)
    open_file(1, 2, 3)
    open_file(filename='file1.txt')
    open_file()
    logger.info('This is an info message')

    try:
        raise_error()
    except ValueError:
        pass


    @log
    def test(dct):
        return dct

    test({i: i+1 for i in range(20)})

    @log
    def test_np_array(ar):
        return ar

    test_np_array(np.array(['a', 'a', 1, 1, 2]))
    test_np_array(np.arange(10))

    @log
    def test_df(df):
        return df
    
    # Creating a small DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }

    df = pd.DataFrame(data)
    test_df(df)

    test_np_array(np.array(['a', 'a', 1, 1, 2]))

    with open(log_path, 'a') as f:
        f.write("==== End of Execution ====\n")