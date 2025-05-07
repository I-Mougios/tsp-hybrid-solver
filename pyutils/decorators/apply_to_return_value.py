from typing import Callable, TypeVar, Any

R = TypeVar("R")  # Return type of the wrapped function
U = TypeVar("U")  # Type returned after applying `fn`

def apply_to_return_value(fn: Callable[[R], U]) -> Callable[[Callable[..., R]], Callable[..., U]]:
    """A decorator that applies a function `fn` to the return value of another function.
    
    Args:
        fn (Callable[[R], U]): A function that transforms the return value of the wrapped function.

    Returns:
        Callable[[Callable[..., R]], Callable[..., U]]: A decorator that modifies the return value.
    """
    def decorator(inner_function: Callable[..., R]) -> Callable[..., U]:
        def wrapper(*args: Any, **kwargs: Any) -> U:
            inner_function_output = inner_function(*args, **kwargs)
            returned_value = fn(inner_function_output)
            return returned_value
        return wrapper
    return decorator
