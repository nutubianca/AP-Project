from Domain.card import Card
from Domain.cardError import CardError


class CardValidation:
    @staticmethod
    def validation(card: Card):
        errors = []
        if len(card.CNP) != 13:
            errors.append("CNP-ul nu este valid!")
        if not card.CNP.isnumeric():
            errors.append("CNP-ul trebuie sa conntina doar cifre!")
        if card.points < 0:
            errors.append("Punctele acumulate nu sunt negative!")
        if len(errors) > 0:
            raise CardError(errors)
