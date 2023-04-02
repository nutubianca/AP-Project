from Domain.film import Film
from Domain.filmError import FilmError


class FilmValidation:
    def validation(self, film: Film):
        errors = []
        if film.ticketPrice <= 0:
            errors.append("Pretul trebuie sa fie strict mai mare decat 0!")
        if film.inSchedule not in ["da", "nu",  "Da", "Nu"]:
            errors.append("Folositi doar da/nu la optiunea 'in program'!")
        if len(errors) > 0:
            raise FilmError(errors)
