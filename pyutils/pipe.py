from typing import Callable, Any
from .logger import log


class Pipe(object):
    def __init__(self, callables: list[Callable[..., Any]],
                 debug=False):
        
        if not callables:
            raise ValueError("Pipe must have at least one function.")

        if debug:
            self._callables = [log(callable) for callable in callables]
        else:
            self._callables = callables

    
    def __call__(self, *args, **kwargs):
        """
        Executes the sequence of callables in the pipe.
        Arguments are passed to the first callable, and the output of each callable is passed as input to the next.
        With that said the first callable can receive multiple arguements and the rest of the callables can receive only one argument.
        If multiple arguments must be passed in other callables other than the first one, those must be passed as tuples and be unpacked
        from the callable.

        Args:
            *args: Positional arguments to pass to the first callable.
            **kwargs: Keyword arguments to pass to the first callable.

        Returns:
            The output of the last callable in the sequence after processing.

        Raises:
            Any exception raised by the callables in the sequence.
        """
        output =  self.callables[0](*args, **kwargs)
        for callable in self.callables[1:]:
            output = callable(output)
        return output
    
    @property
    def callables(self):
        return self._callables
    
if __name__ == '__main__':

    # Example function that we can use in the Pipe
    def add_one(x):
        return x + 1

    def multiply_by_two(x):
        return x * 2

    def subtract_three(x):
        return x - 3

    # Test if the Pipe class works correctly
    def test_pipe_operations():
        # Test 1: Simple operations without debug logging
        pipe = Pipe([add_one, multiply_by_two, subtract_three])

        result = pipe(5)
        assert result == 9, f"Expected 7, but got {result}"  # (5 + 1) * 2 - 3 = 7
        
        # Test 2: Test with debug flag set to True (logging functions)
        pipe_debug = Pipe([add_one, multiply_by_two, subtract_three], debug=True)
        
        # Since we don't want to manually check the logs, we can focus on functionality
        result_debug = pipe_debug(10)
        assert result_debug == 19, f"Expected 19, but got {result_debug}"  # (10 + 1) * 2 - 3 = 17

    test_pipe_operations()



    
    

        