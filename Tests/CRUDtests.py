from Domain.card import Card
from Domain.film import Film
from Domain.reservation import Reservation
from datetime import datetime
from Repository.repositoryJson import RepositoryJson


def test_crud_film():
    file = "fileForTests.json"
    open(file, "w").close()
    film_rep = RepositoryJson(file)
    assert film_rep.read("2") is None
    film = Film("1", "Titanic",
                datetime.strptime("1997", "%Y"),
                25, "da")
    film_rep.adding(film)
    assert film_rep.read("1") == film
    film_rep.deleting("1")
    assert film_rep.read("1") is None


def test_crud_card():
    file = "fileForTests.json"
    open(file, "w").close()
    card_rep = RepositoryJson(file)
    card = Card("2", "Popescu", "Maria",
                "6030215345912",
                datetime.strptime("11.04.2002", "%d.%m.%Y"),
                datetime.strptime("23.05.2021", "%d.%m.%Y"),
                5)
    card_rep.adding(card)
    assert card_rep.read("2") is not None
    card_rep.deleting("2")
    assert card_rep.read("2") is None


def test_crud_reservation():
    file = "fileForTests.json"
    open(file, "w").close()
    res_rep = RepositoryJson(file)
    reservation = Reservation(
        "7", "2", "1",
        datetime.strptime("12.12.2021 12:45",
                          "%d.%m.%Y %H:%M"))
    res_rep.adding(reservation)
    assert res_rep.read("7") is not None
    res_rep.deleting("7")
    assert res_rep.read("7") is None
    open(file, "w").close()
