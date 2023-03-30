from dataclasses import dataclass
from datetime import datetime
from Domain.entitate import Entitate


@dataclass
class Film(Entitate):
    title: str
    yearOfApparition: datetime
    ticketPrice: float
    inSchedule: str
