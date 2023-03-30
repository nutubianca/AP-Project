from Domain.addOp import AddOp
from Domain.cardValidation import CardValidation
from Domain.cascadaOp import CascadaOp
from Domain.deleteOp import DeleteOp
from Domain.modifyOp import ModifyOp
from Domain.multiDeleteOp import MultiDeleteOp
from Domain.resValidation import ResValidation
from Domain.reservation import Reservation
from Repository.repository import Repository
from Service.cardService import CardService
from Service.undoRedoService import UndoRedoService


class ResService:
    def __init__(self,
                 resRepository: Repository,
                 resValidation: ResValidation,
                 cardRepository: Repository,
                 filmRepository: Repository,
                 undoRedoService: UndoRedoService):
        self.__resRepository = resRepository
        self.__resValidation = resValidation
        self.__cardRepository = cardRepository
        self.__filmRepository = filmRepository
        self.__undoRedoService = undoRedoService

    def get_all(self):
        return self.__resRepository.read()

    def get_by_index(self, idRes):
        return self.__resRepository.read(idRes)

    def adding(self, idRes, idFilm, idClient, dateAndTime):
        res = Reservation(idRes, idFilm, idClient, dateAndTime)
        self.__resValidation.validation(res)

        film = self.__filmRepository.read(idFilm)
        if not film:
            raise KeyError("Nu exista un film cu id-ul dat!")
        if film.inSchedule == "nu":
            raise KeyError("Filmul nu se afla in program!")
        card_verifcare = self.__cardRepository.read(idClient)
        if not card_verifcare:
            raise KeyError("Nu exista un card cu id-ul dat!")
        card_validation = CardValidation()
        card_service = CardService(self.__cardRepository, card_validation,
                                   self.__undoRedoService)
        card_service.bonus_points(
            card_service.get_by_index(idClient),
            film.ticketPrice
        )
        self.__resRepository.adding(res)
        self.__undoRedoService.add_undoOp(AddOp(
            self.__resRepository, res)
        )

    def deleting(self, idRes):
        reservation = self.__resRepository.read(idRes)
        film = self.__filmRepository.read(reservation.idFilm)
        card_validation = CardValidation()
        card_service = CardService(self.__cardRepository, card_validation,
                                   self.__undoRedoService)
        if card_service.get_by_index(reservation.idClient):
            card_service.retreat_bonus_points(
                card_service.get_by_index(reservation.idClient),
                film.ticketPrice
            )
        self.__resRepository.deleting(idRes)
        self.__undoRedoService.add_undoOp(DeleteOp(
            self.__resRepository,
            reservation
        ))

    def modify(self, idRes, idFilm, idClient, dateAndTime):
        res = Reservation(idRes, idFilm, idClient, dateAndTime)
        old_one = self.get_by_index(idRes)
        self.__resValidation.validation(res)
        self.__resRepository.modify(res)
        self.__undoRedoService.add_undoOp(ModifyOp(
            self.__resRepository, res, old_one)
        )

    @staticmethod
    def verify_schedule(in_program):
        if in_program == "nu":
            raise ValueError("Filmul nu se afla in program!")

    def sortingAfterRes(self):
        '''
        - sorteaza descrescator un dictionar cu filmele
         din memorie, dupa numarul de rezervari
        :return: lista de dictionare sortata, conform cerintei
        '''
        res_per_film = {}
        rezultat = []
        for film in self.__filmRepository.read():
            res_per_film[film.idEntitate] = ["0"]

        for reservation in self.__resRepository.read():
            res_per_film[reservation.idFilm].append("1")
        for film in self.__filmRepository.read():
            rezultat.append({
                "film": film,
                "numar_de_rezervari": res_per_film[film.idEntitate].count("1")
            })
        return sorted(rezultat,
                      key=lambda res_per_film: res_per_film
                      ["numar_de_rezervari"],
                      reverse=True)

    def if_between_hours(self, hour1, hour2, hour):
        if hour1.hour <= hour.hour:
            if hour.hour < hour2.hour:
                return True
            elif hour.hour == hour2.hour:
                if hour1.minute <= hour.minute <= hour2.minute:
                    return True

    def take_between_hours(self, hour1, hour2):
        '''
        -gaseste rezervarile dintr-un interval de ore dat,
        indiferent de zi
        :param hour1: prima ora din interval
        :param hour2: a doua ora din interval
        :return: lista cu entitatile de tip 'reservation'
         care se incadreaza in intervalul de ore dat
        '''
        rezultat = [reservation for reservation
                    in self.__resRepository.read()
                    if self.if_between_hours(
                        hour1,
                        hour2,
                        reservation.dateAndTime)]
        return rezultat

    def delete_between_days(self, day1, day2):
        '''
        -efectueaza stergerea entitatilor de tip 'reservation'
        care sunt intr-un anumit interval de zile, dat de
        utilizator
        :param day1: prima zi din interval
        :param day2: a doua zi din interval
        '''
        lista = []
        for reservation in self.__resRepository.read():
            day = reservation.dateAndTime.day
            if day1.day <= day <= day2.day:
                lista.append(reservation)
                self.deleting(reservation.idEntitate)
        self.__undoRedoService.add_undoOp(MultiDeleteOp(
            self.__resRepository, lista
        ))

    def find_film_res(self, idFilm):
        lista = []
        for reservation in self.__resRepository.read():
            if reservation.idFilm == idFilm:
                lista.append(reservation.idEntitate)
        return lista

    def deleted_film_res(self, idFilm):
        lista = self.find_film_res(idFilm)
        lista_res = []
        film = self.__filmRepository.read(idFilm)
        self.__filmRepository.deleting(idFilm)
        for resId in lista:
            lista_res.append(
                self.__resRepository.read(resId)
            )
            self.__resRepository.deleting(resId)
        self.__undoRedoService.add_undoOp(CascadaOp(
            self.__filmRepository, self.__resRepository,
            film, lista_res
        ))
