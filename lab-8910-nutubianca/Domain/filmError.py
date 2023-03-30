from dataclasses import dataclass


@dataclass
class FilmError(Exception):
    mesaj: str

    def __str__(self):
        return f'FilmError: : {self.mesaj}'
