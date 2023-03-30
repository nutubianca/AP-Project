from Domain.cardValidation import CardValidation
from Domain.filmValidation import FilmValidation
from Domain.resValidation import ResValidation
from Domain.undoRedoOp import UndoRedoOp
from Repository.repositoryJson import RepositoryJson
from Service.cardService import CardService
from Service.filmService import FilmService
from Service.resService import ResService
from Service.undoRedoService import UndoRedoService
from Tests.AllTests import all_tests
from UI.console import Console


def main():
    all_tests()
    filmRepositoryJson = RepositoryJson("films.json")
    cardRepositoryJson = RepositoryJson("cards.json")
    resRepositoryJson = RepositoryJson("reservations.json")

    filmValidation = FilmValidation()
    cardValidation = CardValidation()
    resValidation = ResValidation()

    undoRedoService = UndoRedoService()

    resService = ResService(resRepositoryJson, resValidation,
                            cardRepositoryJson, filmRepositoryJson,
                            undoRedoService)
    filmService = FilmService(filmRepositoryJson, filmValidation,
                              resService, undoRedoService)
    cardService = CardService(cardRepositoryJson, cardValidation,
                              undoRedoService)
    console = Console(filmService, cardService,
                      resService, undoRedoService)

    console.runMenu()


main()
