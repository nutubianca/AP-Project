from Domain.addOp import AddOp
from Domain.deleteOp import DeleteOp
from Domain.film import Film
from Domain.filmValidation import FilmValidation
import random
from datetime import datetime
from Domain.modifyOp import ModifyOp
from Repository.repository import Repository
from Service.resService import ResService
from Service.undoRedoService import UndoRedoService


class FilmService:
    def __init__(self,
                 filmRepository: Repository,
                 filmValidation: FilmValidation,
                 resService: ResService,
                 undoRedoService: UndoRedoService):
        self.__filmRepository = filmRepository
        self.__filmValidation = filmValidation
        self.__resService = resService
        self.__undoRedoService = undoRedoService

    def get_all(self):
        return self.__filmRepository.read()

    def get_by_index(self, idFilm):
        return self.__filmRepository.read(idFilm)

    def adding(self, idFilm, title, yearOfApparition, ticketPrice, inSchedule):
        film = Film(idFilm, title, yearOfApparition, ticketPrice, inSchedule)
        self.__filmValidation.validation(film)
        self.__filmRepository.adding(film)
        self.__undoRedoService.add_undoOp(AddOp(self.__filmRepository, film))

    def deleting(self, idFilm):
        self.__resService.deleted_film_res(idFilm)
        '''self.__undoRedoService.add_undoOp(DeleteOp(
            self.__filmRepository,
            film))'''

    def modify(self, idFilm, title, yearOfApparition, ticketPrice, inSchedule):
        film = Film(idFilm, title, yearOfApparition, ticketPrice, inSchedule)
        old_one = self.get_by_index(idFilm)
        self.__filmValidation.validation(film)
        self.__filmRepository.modify(film)
        self.__undoRedoService.add_undoOp(ModifyOp(self.__filmRepository,
                                                   film, old_one))

    def random_generator(self, how_many):
        '''
        -genereaza entitati de tip 'film'
        :param how_many: numar de tip int ce reprezinta
         numarul de generari dorite de utilizator
        '''
        lists_of_films = ["Avatar", "Cars", "Thor", "IronMan", "HungerGames",
                          "Wonder", "Count of Monte Cristo"]
        lists_of_years = ["2009", "2006", "2011", "2008", "2012",
                          "2017", "2002"]
        inSch = ["da", "nu"]
        random_list = random.sample(range(1, 7), how_many)
        for nr in random_list:
            self.adding(str(nr), lists_of_films[nr],
                        datetime.strptime(lists_of_years[nr], "%Y"),
                        random.randint(20, 35),
                        random.choice(inSch))

    def film_searching(self, given_string: str):
        '''
        -cauta string ul 'given_string' in toate atributele obiectelor 'film'
        :param given_string: textul de tip str ce va fi cautat
         in entitatile de tip 'film'
        :return: returneaza lista de obiecte in care se regaseste given_string
        '''
        lista = []
        for film in self.__filmRepository.read():
            inFilm = False
            if given_string in str(film.idEntitate):
                inFilm = True
            elif given_string in film.title:
                inFilm = True
            elif given_string in film.yearOfApparition.strftime("%Y"):
                inFilm = True
            elif given_string in str(film.ticketPrice):
                inFilm = True
            elif given_string in film.inSchedule:
                inFilm = True

            if inFilm:
                lista.append(film)
        return lista
