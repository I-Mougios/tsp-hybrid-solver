# validator.py
import weakref
import json
from collections import defaultdict
from types import MappingProxyType
from numbers import Real
from datetime import date, datetime
from .decorators import Dispatcher

__all__ = ['validate', 'TypeChecker', 'ValidationError']

class ValidationError(ValueError):
    """
    Custom exception to log validation errors for incorrect values.

    Attributes:
        field_name (str): The name of the field where the validation error occurred.
        error_message (str): A descriptive error message indicating the validation issue.
        all (defaultdict): A class-level attribute that maps field names to lists of error messages.
    """
    all = defaultdict(list)

    def __init__(self, error_message: str=None, field_name: str=None ):
        """
        Initializes a ValidationError instance and logs the error.

        Args:
            field_name (str): The name of the field where the validation error occurred.
            error_message (str): A descriptive message indicating the validation issue.
        """
        super().__init__(error_message)
        self.error_message = error_message
        self.field_name = field_name



    @classmethod
    def get_errors(cls):
        """
        Retrieve all logged validation errors.

        Returns:
            MappingProxy: A read-only dictionary mapping field names to their respective error messages.
        """
        return MappingProxyType(cls.all)

    @classmethod
    def clear_errors(cls):
        """
        Clear all logged validation errors.
        """
        cls.all.clear()

    @classmethod
    def to_json(cls):
        """
        Convert the `all` attribute to a JSON string.

        Returns:
            str: A JSON string representing all logged validation errors.
        """
        return json.dumps(cls.get_errors().copy(),
                          indent=4,
                          default= ValidationError.json_format)

    @staticmethod
    def json_format(obj):
        return obj.error_message



@Dispatcher
def validate(*args, **kwargs):
    try:
        key = args[0]
    except IndexError as e:
        raise ValueError('At least one of the arguments is required')

    raise KeyError(f"No validation function registered for type {type(args[0])}."
                   f" Please register one to handle this type.")


@validate.register(str)
def validate_string(type_, value, attr_name, *, min_length, max_length, **kwargs):
    if value is None:
        return True, ""
    if not isinstance(value, str):
        return False, ValidationError(error_message=f'Field {attr_name} is type of str. Invalid value: {value}',
                                      field_name=attr_name)
    if min_length and len(value) <= min_length:
        return False, ValidationError(error_message=f"Field {attr_name} must have at least {min_length} characters."
                                                    f" Invalid value: {value}",
                                      field_name=attr_name)
    if max_length and len(value) >= max_length:
        return False, ValidationError(error_message=f"Field {attr_name} cannot have more than {max_length} characters."
                                                    f" Invalid value: {value}",
                                      field_name=attr_name)
    return True, ""


@validate.register(int)
def validate_integer(type_, value, attr_name, *, min_value, max_value, **kwargs):
    if value is None:
        return True, ""
    if not isinstance(value, Real) or float(value) != int(value):
        return False, ValidationError(error_message=f"{attr_name} is type of integer. Invalid value: {value}",
                                      field_name=attr_name)
    if not (min_value < value < max_value):
        return False, ValidationError(error_message=f"{attr_name} must be between {min_value} and {max_value}."
                                                    f" Bottom and upper bounds inclusive",
                                      field_name=attr_name)
    return True, ""


@validate.register(float)
def validate_float(type_, value, attr_name, *, min_value=None, max_value=None, max_length=None, **kwargs):
    if value is None:
        return True, ""
    if not isinstance(value, Real):
        return False, ValidationError(error_message=f"{attr_name} must be a float. Invalid value: {value}",
                                      field_name=attr_name)
    if not (min_value < value < max_value):
        return False, ValidationError(error_message= f"{attr_name} must be between {min_value} and {max_value}."
                                                 f" Bottom and upper bounds inclusive. Invalid value: {value}",
                                      field_name=attr_name)
    if max_length is not None:
        # Split the float into its integer and decimal parts
        parts = str(value).split(".")
        if len(parts) > 1 and len(parts[1]) > max_length:
            return False, ValidationError(error_message=f"{attr_name} must have at most {max_length} decimal places."
                                                        f" Invalid value: {value}",
                                          field_name=attr_name)
    return True, ""


@validate.register(date)
def validate_date(type_, value, attr_name, *, acceptable_formats=None, **kwargs):
    """
    Validate a date string with specified acceptable formats.

    Args:
        value: The value to validate (date string).
        attr_name: The attribute name being validated.
        acceptable_formats: A list of acceptable date formats (default: ['%Y%m%d', '%Y-%m-%d']).

    Returns:
        Tuple (bool, str or ValidationError): Validation status and message or error object.
    """
    if value is None or isinstance(value, (date, datetime)):
        return True, ""
    if acceptable_formats is None:
        acceptable_formats = ['%Y%m%d', '%Y-%m-%d']

    for fmt in acceptable_formats:
        try:
            # Try parsing the value with each format
            datetime.strptime(value, fmt)
            return True, ""
        except ValueError:
            continue

    # If no formats match, return a validation error
    return False, ValidationError(error_message=f"{attr_name} must match one of the formats:"
                                                f" {', '.join(acceptable_formats)}. Invalid value: {value}",
                                  field_name=attr_name)


@validate.register('enum')
def validate_enum(type_, value, attr_name, enum_list, **kwargs):
    if value is None:
        return True, ""
    if enum_list is None:
        raise ValueError('Enum list can not be empty. Provide the acceptable values for attribute {attr_name}')
    if value not in enum_list:
        return False, ValidationError(error_message=f"Acceptable values for attribute {attr_name} are {enum_list}."
                                                    f" Invalid value: {value}",
                                      field_name=attr_name)

    return True, ""



class TypeChecker:
    """
    A descriptor to validate and enforce type and value constraints on an attribute.

    Attributes:
        type_ (type): The expected type of the attribute.
        min_length (Optional[int]): Minimum length for the value if it is a sequence (e.g., list, string).
        max_length (Optional[int]): Maximum length for the value if it is a sequence.
        min_value (Optional[float]): Minimum value for numeric attributes.
        max_value (Optional[float]): Maximum value for numeric attributes.
        required (bool): Whether the attribute is mandatory.
        values (dict): Stores validated values with weak references to their owning instances.
        
    """

    # The validation function can be overwritten, but it should accept a part of the arguments that are specified in the
    # __init__ method of the TypeChecker
    validation_function = staticmethod(validate)

    def __init__(self, type_, min_length=None, max_length=None,
                 min_value=float('-inf'), max_value=float('inf'),
                 required=False, acceptable_date_formats=None,
                 enum_list=None):
        """
        Initializes the TypeChecker with the specified constraints.

        Args:
            type_ (type): The expected data type of the attribute.
            min_length (Optional[int]): Minimum allowed length for the value (if applicable).
            max_length (Optional[int]): Maximum allowed length for the value (if applicable).
            min_value (Optional[float]): Minimum allowed value for numeric attributes.
            max_value (Optional[float]): Maximum allowed value for numeric attributes.
            required (bool): Whether the attribute is mandatory.
            acceptable_date_formats (list(str)): The acceptable format for dates
            
        """
        self.type = type_
        self.min_length = min_length
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value
        self.required = required
        self.acceptable_date_formats = acceptable_date_formats
        self.enum_list = enum_list
        self.log_missing_mandatory_values = True
        self.values = {}
        

    def __set_name__(self, owner_class, attr_name):
        """Assigns the attribute name to the descriptor."""
        self.attr_name = attr_name

    def __get__(self, instance, owner_class):
        """
        Retrieves the value of the attribute for the given instance.

        Args:
            instance: The instance of the owner class.
            owner_class: The owner class where the descriptor is defined.

        Returns:
            The stored value for the instance or None if no value is set.
        """
        if instance is None:
            return self
        tuple_value = self.values.get(id(instance), None)
        return tuple_value[1] if tuple_value else None

    def __set__(self, instance, value):
        """
        Validates and sets the value of the attribute for the given instance.

        Args:
            instance: The instance of the owner class.
            value: The value to set.

        """
        # Case 1: Missing mandatory value
        if value is None and self.required:
            if self.log_missing_mandatory_values:
                self.log_missing_mandatory_values = False
                error = ValidationError(error_message=f'Field {self.attr_name} is mandatory.'
                                                      f' Ensure there are no missing values',
                                        field_name=self.attr_name)
                ValidationError.all[self.attr_name].append(error)
            self.values[id(instance)] = weakref.ref(instance, self._finalise_object), value
            return

        # Case 2: Mandatory and non-missing value or optional
        is_ok, error = self.validation_function(self.type, # Needed to make the dispatching
                                                value,
                                                attr_name=self.attr_name,
                                                min_value=self.min_value,
                                                max_value =self.max_value,
                                                min_length=self.min_length,
                                                max_length=self.max_length,
                                                acceptable_formats = self.acceptable_date_formats,
                                                enum_list = self.enum_list
                                                )

        # Case 3: Log error if validation fails
        if not is_ok:
            ValidationError.all[self.attr_name].append(error)

        # store the value even when an error occured
        self.values[id(instance)] = weakref.ref(instance, self._finalise_object), value

    @classmethod
    def set_validator_function(cls, validator_function):
        validator_function = staticmethod(validator_function)
        cls.validation_function = validator_function
        return validator_function

    def _finalise_object(self, instance_weakref):
        """Removes the weak reference to the instance when it is garbage collected(no more strong references to the object)."""
        reverse_lookup = [key for key, value in self.values.items()
                          if value[0] == instance_weakref]
        key = reverse_lookup[0]
        del self.values[key]




if __name__ == '__main__':


    class Person:
        __slots__ = '__weakref__'

        first_name = TypeChecker(str, min_length=1, max_length=6, required=True)
        last_name = TypeChecker(str, min_length=3, max_length=4, required=True)
        dob = TypeChecker(date, required=True)
        age = TypeChecker(int, min_value=0, max_value=100, required=True)
        salary = TypeChecker(float, min_value=0, max_value=100_000, max_length=2)
        eye_color = TypeChecker('enum', enum_list=['brown', 'red', 'black', 'green'])

        def __init__(self, first_name, last_name, dob, age, salary, eye_color=None):
            self.first_name = first_name
            self.last_name = last_name
            self.dob = dob
            self.age = age
            self.salary = salary
            self.eye_color = eye_color


    p1 = Person('Ioannis', 'Mougios','19950727', 100, 100.50, 'brown') # length error in first and last name
    p2 = Person('Joe', None, '2000-05-30', 101, 100.33, 'red') # Missing last_name and age is outlier
    p3 = Person('Joe', None, '2000/05/30', 30, 100.623, 'black') # No logging for missing last name , wrong date format, wrong precision in salary
    p4 = Person('Ema', 'Rose', '1.1.2000', 20, 1000.1, 'rose') # wrong date, wrong eye's color
    p5 = Person('Eric','Boo', '20000101', 24, 1000.03, 'green') # Correct


    for key, value in ValidationError.get_errors().items():
        print(key, value, end='\n'*2)