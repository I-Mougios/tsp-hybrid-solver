# In[0]: Imports
from functools import singledispatch
from numbers import Real
from decimal import Decimal

# In [1]: Definition of trim_whitespace decorator
class UnregisteredKey(KeyError):
    """
    Exception raised when an unregistered datatype is passed to `trim_characters`.

    This error occurs when a function is called with a data type that has 
    not been explicitly registered using `@trim_characters.register`.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message="The provided datatype is not registered. Use @trim_characters.register to define behavior for this type."):
        super().__init__(message)


@singledispatch
def trim_whitespaces(obj, **kwargs):
    """
    Trims characters from a given argument based on its type.

    This function uses `functools.singledispatch` to delegate operations
    based on the type of the first input argument. If the type is unregistered,
    an `UnregisteredKey` exception is raised.

    Args:
        obj: The input whose type determines the function behavior.

    Raises:
        UnregisteredKey: If no function is registered for `type(obj)`.
    """
    raise UnregisteredKey(f"The provided datatype {type(obj)} is not registered. Use @trim_whitespaces.register to define behavior for this type.")

@trim_whitespaces.register
def _(obj: str, **kwargs) -> str:
    """
    Removes leading or trailing whitespaces.
    Behind the hood it uses the .strip() method
    """
    return obj.strip()

@trim_whitespaces.register(Real)
@trim_whitespaces.register(int)
@trim_whitespaces.register(float)
@trim_whitespaces.register(Decimal)
def _(obj: Real, **kwargs) -> Real:
    """Return the real number intact"""
    return obj

@trim_whitespaces.register
def _(obj: dict, **kwargs) -> dict:
    """Removes trailing and leading whitespaces for both keys and values"""
    new_dict = {}
    for key, value in obj.items():
       new_key, new_value = trim_whitespaces(key, **kwargs), trim_whitespaces(value, **kwargs)
       new_dict[new_key] = new_value
    
    return new_dict


@trim_whitespaces.register(tuple)
@trim_whitespaces.register(list)
def _(obj, **kwargs):
    """Removes whitespaces from the elements inside the subscriptable iterables"""
    iterable_type = type(obj)
    homogenous = kwargs.get('homogenous', False)
    if homogenous and obj:
        # If the iterable is homogenous, we can find the type of the first element and apply the 
        # registered function by doing the lookup to registry only one time.
        # As Fallback in case of unregistered dtype take the default function so it wll return the custom error message.
        # Notice that the dtype Real encompasses int, float and Decimal but when it comes to get the corresponding function for
        # int, float or Decimal it will return the default function(value) specified in the get method.
        fn = trim_whitespaces.registry.get(type(obj[0]), trim_whitespaces)
        generator = (fn(value, **kwargs) for value in obj)
    else:
        generator = (trim_whitespaces(value, **kwargs) for value in obj)
    return iterable_type(generator)



@trim_whitespaces.register(set)
@trim_whitespaces.register(frozenset)
def _(obj, **kwargs):
    iterable_type = type(obj)
    homogenous = kwargs.get('homogenous', False)
    if homogenous and obj:
        # If the iterable is homogenous, we can find the type of the first element and apply the 
        # registered function for doing the lookup to registry only one time
        fn = trim_whitespaces.registry.get(next(iter(obj)), trim_whitespaces)
        generator = (fn(value, **kwargs) for value in obj)
    else:
        generator = (trim_whitespaces(value, **kwargs) for value in obj)
    return iterable_type(generator)

