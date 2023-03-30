from dataclasses import dataclass


@dataclass
class CardError(Exception):
    mesaj: str

    def __str__(self):
        return f'CardError: : {self.mesaj}'
