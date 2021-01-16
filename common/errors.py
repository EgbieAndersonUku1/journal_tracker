from dataclasses import dataclass
from wtforms.validators import ValidationError


@dataclass
class CouldNotLogUserActivity(Exception):
    message: str


@dataclass
class CouldNotSaveDataToDatabase(Exception):
    message: str
    

@dataclass
class FailedToSendEmail(Exception):
    message: str



@dataclass
class InvalidUsernameFormat(ValidationError):
    message: str



@dataclass
class UsernameAlreadyExists(ValidationError):
    message: str


@dataclass
class EmailAdressAlreadyExists(ValidationError):
    message: str

