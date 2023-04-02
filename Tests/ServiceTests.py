from Domain.card import Card
from datetime import datetime
from Domain.cardValidation import CardValidation
from Domain.film import Film
from Domain.filmValidation import FilmValidation
from Domain.resValidation import ResValidation
from Domain.reservation import Reservation
from Repository.repositoryJson import RepositoryJson
from Service.cardService import CardService
from Service.filmService import FilmService
from Service.resService import ResService
from Service.undoRedoService import UndoRedoService


def date_pentru_testare():
    open("cardTest.json", "w").close()
    open("filmTest.json", "w").close()
    open("resTest.json", "w").close()

    film_rep = RepositoryJson("filmTest.json")
    res_rep = RepositoryJson("resTest.json")
    card_rep = RepositoryJson("cardTest.json")

    card1 = Card("1", "Popescu", "Maria", "6020501982428",
                 datetime.strptime("1.05.2002", "%d.%m.%Y"),
                 datetime.strptime("15.10.2021", "%d.%m.%Y"),
                 3)
    card2 = Card("2", "Clipa", "Ioana", "6010613220456",
                 datetime.strptime("13.06.2001", "%d.%m.%Y"),
                 datetime.strptime("1.11.2021", "%d.%m.%Y"),
                 5)
    card_rep.adding(card1)
    card_rep.adding(card2)

    film = Film("1", "Titanic",
                datetime.strptime("1997", "%Y"),
                25, "da")
    film_rep.adding(film)

    film = Film("2", "IronMan",
                datetime.strptime("2008", "%Y"),
                35, "da")
    film_rep.adding(film)

    reservation = Reservation(
        "1", "2", "1",
        datetime.strptime("12.12.2021 12:45",
                          "%d.%m.%Y %H:%M"))
    res_rep.adding(reservation)

    reservation = Reservation(
        "2", "2", "2",
        datetime.strptime("12.12.2021 12:30",
                          "%d.%m.%Y %H:%M"))
    res_rep.adding(reservation)

    reservation = Reservation(
        "3", "1", "1",
        datetime.strptime("14.12.2021 12:05",
                          "%d.%m.%Y %H:%M"))
    res_rep.adding(reservation)


def test_sorting_by_points():
    card_rep = RepositoryJson("cardTest.json")

    file = "cardTest.json"
    open(file, "r").close()
    dict_verify = sorted(card_rep.read(),
                         key=lambda card: card.points,
                         reverse=True)
    assert dict_verify[0] == card_rep.read("2")
    assert dict_verify[1] == card_rep.read("1")


def test_add_a_point():
    open("cardTest.json", "r").close()
    card_rep = RepositoryJson("cardTest.json")
    card_validation = CardValidation()
    undoRedo = UndoRedoService()
    card_service = CardService(
        card_rep, card_validation, undoRedo)

    card_service.add_a_point(datetime.strptime(
                "25.04.2002", "%d.%m.%Y"),
                datetime.strptime(
                "25.05.2002", "%d.%m.%Y"), 10)
    assert card_rep.read("1").points == 13
    assert card_rep.read("2").points == 5


def test_card_searching():
    open("cardTest.json", "r").close()
    card_rep = RepositoryJson("cardTest.json")
    card_validation = CardValidation()
    undoRedo = UndoRedoService()
    card_service = CardService(
        card_rep, card_validation, undoRedo)

    lista = card_service.card_searching("60")
    assert lista[0] == card_rep.read("1")
    assert lista[1] == card_rep.read("2")

    lista = card_service.card_searching("Popescu")
    assert lista[0] == card_rep.read("1")
    assert len(lista) == 1


def test_film_searching():
    open("filmTest.json", "r").close()
    film_rep = RepositoryJson("filmTest.json")
    res_rep = RepositoryJson("resTest.json")
    card_rep = RepositoryJson("cardTest.json")

    res_Validation = ResValidation()
    film_validation = FilmValidation()
    undoRedo = UndoRedoService()

    res_service = ResService(res_rep, res_Validation,
                             card_rep, film_rep,
                             undoRedo)
    film_service = FilmService(film_rep, film_validation,
                               res_service, undoRedo)

    lista = film_service.film_searching("2008")
    assert lista[0] == film_rep.read("2")
    assert len(lista) == 1


def test_sorting_after_res():
    open("resTest.json", "r").close()
    open("filmTest.json", "r").close()
    film_rep = RepositoryJson("filmTest.json")
    res_rep = RepositoryJson("resTest.json")
    card_rep = RepositoryJson("cardTest.json")
    res_Validation = ResValidation()
    undoRedo = UndoRedoService()
    res_service = ResService(res_rep, res_Validation,
                             card_rep, film_rep,
                             undoRedo)
    lista = res_service.sortingAfterRes()
    assert lista[0]["film"] == film_rep.read("2")
    assert lista[1]["film"] == film_rep.read("1")


def test_take_between_hours():
    open("resTest.json", "r").close()
    open("filmTest.json", "r").close()
    film_rep = RepositoryJson("filmTest.json")
    res_rep = RepositoryJson("resTest.json")
    card_rep = RepositoryJson("cardTest.json")
    res_Validation = ResValidation()
    undoRedo = UndoRedoService()
    res_service = ResService(res_rep, res_Validation,
                             card_rep, film_rep, undoRedo)
    rezultat = res_service.take_between_hours(
        datetime.strptime("12:20", "%H:%M"),
        datetime.strptime("12:50", "%H:%M"))
    assert rezultat[0] == res_rep.read("1")
    assert rezultat[1] == res_rep.read("2")


def delete_between_days():
    open("resTest.json", "r").close()
    open("filmTest.json", "r").close()
    film_rep = RepositoryJson("filmTest.json")
    res_rep = RepositoryJson("resTest.json")
    card_rep = RepositoryJson("cardTest.json")
    res_Validation = ResValidation()
    undoRedo = UndoRedoService()
    res_service = ResService(res_rep, res_Validation,
                             card_rep, film_rep, undoRedo)
    res_service.delete_between_days(
        datetime.strptime("11", "%d"),
        datetime.strptime("13", "%d"))
    assert res_rep.read("1") is None
    assert res_rep.read("2") is None
    assert res_rep.read("3") is not None


def test_undo_redo():
    open("resTest.json", "w").close()
    open("filmTest.json", "w").close()
    open("cardTest.json", "w").close()
    res_rep = RepositoryJson("resTest.json")
    card_rep = RepositoryJson("cardTest.json")
    film_rep = RepositoryJson("filmTest.json")
    res_Validation = ResValidation()
    undoRedo = UndoRedoService()
    res_service = ResService(res_rep, res_Validation,
                             card_rep, film_rep, undoRedo)
    card_validation = CardValidation()
    card_service = CardService(card_rep, card_validation,
                               undoRedo)
    card_service.adding(
        "1", "Popescu", "Maria", "6020501982428",
        datetime.strptime("1.05.2002", "%d.%m.%Y"),
        datetime.strptime("15.10.2021", "%d.%m.%Y"), 3)
    card1 = Card(
        "1", "Popescu", "Maria", "6020501982428",
        datetime.strptime("1.05.2002", "%d.%m.%Y"),
        datetime.strptime("15.10.2021", "%d.%m.%Y"), 3)
    undoRedo.undo()
    undoRedo.undo()
    assert card_rep.read() == []
    undoRedo.redo()
    assert card_rep.read() == [card1]

    card_service.deleting(card1.idEntitate)
    undoRedo.undo()
    assert card_rep.read() == [card1]
    undoRedo.redo()
    assert card_rep.read() == []

    undoRedo.undo()
    card_service.modify(
        "1", "Lupescu", "Maria", "6020501982428",
        datetime.strptime("1.05.2002", "%d.%m.%Y"),
        datetime.strptime("15.10.2021", "%d.%m.%Y"), 3)
    card2 = Card(
        "1", "Lupescu", "Maria", "6020501982428",
        datetime.strptime("1.05.2002", "%d.%m.%Y"),
        datetime.strptime("15.10.2021", "%d.%m.%Y"), 3)
    undoRedo.undo()
    assert card_rep.read() == [card1]
    undoRedo.redo()
    assert card_rep.read() == [card2]
    card_service.deleting(card1.idEntitate)

    card1 = Card("1", "Popescu", "Maria", "6020501982428",
                 datetime.strptime("1.05.2002", "%d.%m.%Y"),
                 datetime.strptime("15.10.2021", "%d.%m.%Y"),
                 10)
    card2 = Card("2", "Clipa", "Ioana", "6010613220456",
                 datetime.strptime("13.06.2001", "%d.%m.%Y"),
                 datetime.strptime("1.11.2021", "%d.%m.%Y"),
                 15)
    card_rep.adding(card1)
    card_rep.adding(card2)

    film = Film("1", "Titanic",
                datetime.strptime("1997", "%Y"),
                25, "da")
    film_rep.adding(film)

    film = Film("2", "IronMan",
                datetime.strptime("2008", "%Y"),
                35, "da")
    film_rep.adding(film)

    reservation = Reservation(
        "1", "2", "1",
        datetime.strptime("12.12.2021 12:45",
                          "%d.%m.%Y %H:%M"))
    res_rep.adding(reservation)

    reservation = Reservation(
        "2", "2", "2",
        datetime.strptime("12.12.2021 12:30",
                          "%d.%m.%Y %H:%M"))
    res_rep.adding(reservation)

    reservation = Reservation(
        "3", "1", "1",
        datetime.strptime("14.12.2021 12:05",
                          "%d.%m.%Y %H:%M"))
    res_rep.adding(reservation)
    res_service.delete_between_days(
        datetime.strptime("11", "%d"),
        datetime.strptime("13", "%d"))
    undoRedo.undo()
    assert res_rep.read("1") is not None
    assert res_rep.read("2") is not None
    undoRedo.redo()
    assert res_rep.read("1") is None
    assert res_rep.read("2") is None
    assert res_rep.read("3") is not None

    card_service.add_a_point(datetime.strptime(
        "25.04.2002", "%d.%m.%Y"),
        datetime.strptime(
            "25.05.2002", "%d.%m.%Y"), 10)
    undoRedo.undo()
    assert card_rep.read("1").points == 7
    assert card_rep.read("2").points == 12
    undoRedo.redo()
    assert card_rep.read("1").points == 17
    assert card_rep.read("2").points == 12


def erase_files():
    open("cardTest.json", "w").close()
    open("filmTest.json", "w").close()
    open("resTest.json", "w").close()
    open("fileForTests.json", "w").close()
