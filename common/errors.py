from pydantic.v1 import MissingError
from pydantic.v1.error_wrappers import ErrorWrapper

errors = [
    ErrorWrapper(MissingError(), loc="username"),
    ErrorWrapper(MissingError(), loc="email")
]
