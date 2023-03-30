from dataclasses import dataclass
from datetime import datetime
from Domain.entitate import Entitate


@dataclass
class Card(Entitate):
    name: str
    surname: str
    CNP: str
    birthday: datetime
    date_of_registration: datetime
    points: int
