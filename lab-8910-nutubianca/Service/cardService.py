from Domain.addOp import AddOp
from Domain.card import Card
from Domain.cardValidation import CardValidation
from Domain.deleteOp import DeleteOp
from Domain.modifyOp import ModifyOp
from Domain.multiModifyOp import MultiModifyOp
from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class CardService:
    def __init__(self,
                 cardRepository: Repository,
                 cardValidation: CardValidation,
                 undoRedoService: UndoRedoService):
        self.__cardRepository = cardRepository
        self.__cardValidation = cardValidation
        self.__undoredoService = undoRedoService

    def get_all(self):
        return self.__cardRepository.read()

    def get_by_index(self, idCard):
        return self.__cardRepository.read(idCard)

    def bonus_points(self, card: Card, price):
        card_points = card.points + int(0.1 * price)
        self.modify(card.idEntitate,
                    card.name,
                    card.surname,
                    card.CNP,
                    card.birthday,
                    card.date_of_registration,
                    card_points)

    def retreat_bonus_points(self, card: Card, price):
        card_points = card.points - int(0.1 * price)
        self.modify(card.idEntitate,
                    card.name,
                    card.surname,
                    card.CNP,
                    card.birthday,
                    card.date_of_registration,
                    card_points)

    def adding(self, idCard, name,
               surname, CNP, birthday,
               dateOfRegistration, points):
        card = Card(idCard, name, surname,
                    CNP, birthday,
                    dateOfRegistration,
                    points)
        self.__cardValidation.validation(card)
        self.__cardRepository.adding(card)
        self.__undoredoService.add_undoOp(AddOp(self.__cardRepository,
                                                card))

    def deleting(self, idCard):
        card = self.__cardRepository.read(idCard)
        self.__cardRepository.deleting(idCard)
        self.__undoredoService.add_undoOp(DeleteOp(
            self.__cardRepository,
            card
        ))

    def modify(self, idCard, name,
               surname, CNP,
               birthday,
               dateOfRegistration, points):
        card = Card(idCard, name,
                    surname, CNP,
                    birthday,
                    dateOfRegistration, points)
        old_one = self.get_by_index(idCard)
        self.__cardValidation.validation(card)
        self.__cardRepository.modify(card)
        self.__undoredoService.add_undoOp(ModifyOp(self.__cardRepository,
                                                   card, old_one))

    def add_a_point(self, birthday1, birthday2, given_points):
        '''
        -incrementeaza cu o valoare data a punctelor
         de pe toate cardurile a caror zi de nastere
         se afla in intrevalul dat
        :param birthday1: prima parte din interval, de tip datetime
        :param birthday2: a doua parte din interval, de tip datetime
        :param given_points: valoarea data
        '''
        lista1 = []
        lista2 = []
        for card in self.__cardRepository.read():
            birthday = card.birthday
            if birthday1 <= birthday <= birthday2:
                lista1.append(card)
                card_points = card.points + given_points
                self.modify(card.idEntitate,
                            card.name,
                            card.surname,
                            card.CNP,
                            card.birthday,
                            card.date_of_registration,
                            card_points)
                lista2.append(Card(
                    card.idEntitate,
                    card.name,
                    card.surname,
                    card.CNP,
                    card.birthday,
                    card.date_of_registration,
                    card_points
                ))
        self.__undoredoService.add_undoOp(MultiModifyOp(
            self.__cardRepository, lista2, lista1
        ))

    def mySort(self, lista, key, reverse: bool):
        '''
        _sorteaza o lista dupa o cheie key
        -se poate sorta crescator/descrescator in functie de
        valoarea de adevar a parametrului reverse
        :param lista: lista care urmeaza sa fie sortata
        :param key: valoarea dupa care lista va fi sortata
        :param reverse: crescator(False/descrescator(True)
        :return: lista sortata dupa parametrul key
        '''
        n = len(lista)
        if reverse is False:
            for i in range(n):
                for j in range(1, n):
                    if key(lista[j - 1]) > key(lista[j]):
                        lista[j - 1], lista[j] = lista[j], lista[j - 1]
        elif reverse is True:
            for i in range(n):
                for j in range(1, n):
                    if key(lista[j - 1]) < key(lista[j]):
                        lista[j - 1], lista[j] = lista[j], lista[j - 1]
        return lista

    def sort_by_points(self):
        '''
        -sorteaza cardurile descrescator,
         in functie de numrul de puncte
        :return:  lista sortata descrescator de dictionare
         ce contin entitatile de tip Card
        '''
        return self.mySort(
             self.__cardRepository.read(),
             key=lambda card: card.points,
             reverse=True)

    def add_a_pointt(self, birthday1, birthday2, given_points):
        '''
        -incrementeaza cu o valoare data a punctelor
         de pe toate cardurile a caror zi de nastere
         se afla in intrevalul dat
        :param birthday1: prima parte din interval, de tip datetime
        :param birthday2: a doua parte din interval, de tip datetime
        :param given_points: valoarea data
        '''
        lista1 = []
        lista2 = []
        for card in self.__cardRepository.read():
            birthday = card.birthday
            if birthday1 <= birthday <= birthday2:
                lista1.append(card)
        lista1 = list(map(lambda points: points + given_points,
                          lista1))
        for card in lista1:
            self.modify(card.idEntitate,
                        card.name,
                        card.surname,
                        card.CNP,
                        card.birthday,
                        card.date_of_registration,
                        card.points)
            lista2.append(card)
        self.__undoredoService.add_undoOp(MultiModifyOp(
            self.__cardRepository, lista2, lista1
        ))

    def card_searching(self, given_string):
        '''
        -se cauta un string dat de utilizator in
        cardurile din memorie
        :param text: string-ul dat de la tastatura
        :return: cardul ce contine given_string
        '''
        lista = self.__cardRepository.read()
        return list(filter(
            lambda card: given_string in str(card.idEntitate) or
            given_string in card.name or
            given_string in card.surname or
            given_string in str(card.CNP) or
            given_string in str(card.birthday) or
            given_string in str(card.date_of_registration) or
            given_string in str(card.points),
            lista))
