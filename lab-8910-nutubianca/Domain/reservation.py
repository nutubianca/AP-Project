from dataclasses import dataclass
from datetime import datetime
from Domain.entitate import Entitate


@dataclass
class Reservation(Entitate):
    idFilm: str
    idClient: str
    dateAndTime: datetime
