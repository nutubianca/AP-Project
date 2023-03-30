from Domain.card import Card
from Domain.cardError import CardError
from Domain.film import Film
from Domain.filmError import FilmError
from Service.filmService import FilmService
from Service.resService import ResService
from Service.cardService import CardService
from datetime import datetime

from Service.undoRedoService import UndoRedoService


class Console:
    def __init__(self, filmService: FilmService,
                 cardService: CardService,
                 resService: ResService,
                 undoRedoService: UndoRedoService):
        self.__filmService = filmService
        self.__cardService = cardService
        self.__resService = resService
        self.__undoRedoService = undoRedoService

    def runMenu(self):
        while True:
            print("1. CRUD film")
            print("2. CRUD card client")
            print("3. CRUD rezervare")
            print("4. Generare de un numar ales de filme")
            print("5. Mai multe optiuni")
            print("6. Undo")
            print("7. Redo")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.run_CRUD_film_menu()
            elif optiune == "2":
                self.run_CRUD_card_menu()
            elif optiune == "3":
                self.run_CRUD_rezervare_menu()
            elif optiune == "4":
                self.generare()
            elif optiune == "5":
                self.run_more_options()
            elif optiune == "6":
                self.__undoRedoService.undo()
            elif optiune == "7":
                self.__undoRedoService.redo()
            elif optiune == "x":
                print("Programul se va inchide. Multumim!")
                break
            else:
                print("Optiune inexistenta. Reincercati!")

    def run_CRUD_film_menu(self):
        while True:
            print("1. Adauga film")
            print("2. Sterge film")
            print("3. Modifica film")
            print("a. Afiseaza toate filmele")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.ui_add_film()
            elif optiune == "2":
                self.ui_delete_film()
            elif optiune == "3":
                self.ui_modify_film()
            elif optiune == "a":
                self.show_all_films(
                    self.list_of_films()
                )
            elif optiune == "x":
                print("Submeniul se va inchide.")
                break
            else:
                print("Optiune inexistenta. Reincercati!")

    def run_CRUD_card_menu(self):
        while True:
            print("1. Adauga card client")
            print("2. Sterge card client")
            print("3. Modifica un card client")
            print("a. Afiseaza toate cardurile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.ui_add_card()
            elif optiune == "2":
                self.ui_delete_card()
            elif optiune == "3":
                self.ui_modify_card()
            elif optiune == "a":
                self.show_all_card()
            elif optiune == "x":
                print("Submeniul se va inchide.")
                break
            else:
                print("Optiune inexistenta. Reincercati!")

    def run_CRUD_rezervare_menu(self):
        while True:
            print("1. Adauga rezervare")
            print("2. Sterge rezervare")
            print("3. Modifica rezervare")
            print("a. Afiseaza toate rezervarile")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.ui_add_rezervare()
            elif optiune == "2":
                self.ui_delete_rezervare()
            elif optiune == "3":
                self.ui_modify_rezervare()
            elif optiune == "a":
                self.show_all_rezervare()
            elif optiune == "x":
                print("Submeniul se va inchide.")
                break
            else:
                print("Optiune inexistenta. Reincercati!")

    def ui_add_film(self):
        try:
            idFilm = input("Dati id-ul filmului: ")
            title = input("Dati titlul filmului: ")
            yearOfApparition = datetime.strptime(
                input("Dati anul aparitiei: "), "%Y")
            ticketPrice = float(input("Dati pretul biletului: "))
            inSchedule = input("Mentionati daca este in program(da/nu): ")
            self.__filmService.adding(idFilm, title,
                                      yearOfApparition,
                                      ticketPrice, inSchedule)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
        except FilmError as fe:
            print(fe)

    def ui_delete_film(self):
        try:
            idFilm = input("Dati id-ul filmului de sters: ")
            film = self.__filmService.get_by_index(idFilm)
            self.__filmService.deleting(idFilm)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
        except FilmError as fe:
            print(fe)

    def ui_modify_film(self):
        try:
            idFilm = input("Dati id-ul filmului de modificat : ")
            title = input("Dati noul titlu al filmului: ")
            yearOfApparition = datetime.strptime(
                input("Dati anul nou de aparitie: "), "%Y")
            ticketPrice = float(input("Dati noul pret al biletului: "))
            inSchedule = input("Mentionati daca este in program(da/nu): ")
            self.__filmService.modify(idFilm, title,
                                      yearOfApparition,
                                      ticketPrice, inSchedule)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
        except FilmError as fe:
            print(fe)

    def list_of_films(self):
        lista = []
        for film in self.__filmService.get_all():
            lista.append(film)
        return lista

    def show_all_films(self, lista):
        if len(lista) == 0:
            return 0
        print(lista[0])
        self.show_all_films(lista[1:])

    def ui_add_card(self):
        try:
            idCard = input("Dati id-ul cardului: ")
            name = input("Dati numele clientului: ")
            surname = input("Dati prenumele clientului: ")
            CNP = input("Dati CNP-ul clientului: ")
            birthday = datetime.strptime(
                input("Dati data nasterii clientului: "),
                "%d.%m.%Y")
            dateOfRegistration = datetime.strptime(
                input("Dati data inregistrarii: "),
                "%d.%m.%Y")
            points = int(input("Dati numarul de puncte: "))

            self.__cardService.adding(idCard, name, surname,
                                      CNP, birthday,
                                      dateOfRegistration,
                                      points)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
        except CardError as ce:
            print(ce)

    def ui_delete_card(self):
        try:
            idCard = input("Dati id-ul cardului de sters: ")
            card = self.__cardService.get_by_index(idCard)
            self.__cardService.deleting(idCard)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
        except CardError as ce:
            print(ce)

    def ui_modify_card(self):
        try:
            idCard = input("Dati id-ul cardului de modificat: ")
            name = input("Dati numele clientului: ")
            surname = input("Dati prenumele clientului: ")
            CNP = input("Dati CNP-ul clientului: ")
            birthday = datetime.strptime(
                input("Dati data nasterii clientului: "),
                "%d.%m.%Y")
            dateOfRegistration = datetime.strptime(
                input("Dati data inregistrarii: "),
                "%d.%m.%Y")
            points = int(input("Dati numarul de puncte: "))
            self.__cardService.modify(idCard, name, surname,
                                      CNP, birthday,
                                      dateOfRegistration,
                                      points)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)
        except CardError as ce:
            print(ce)

    def show_all_card(self):
        for card in self.__cardService.get_all():
            print(card)

    def ui_add_rezervare(self):
        try:
            id_res = input("Dati id-ul rezervarii: ")
            id_film = input("Dati id-ul filmului: ")
            id_card = input("Dati id-ul cardului clientului: ")
            data_time = datetime.strptime(
                input("Dati data si ora rezervarii:"),
                "%d.%m.%Y %H:%M")
            self.ui_bonus(self.__cardService.get_by_index(id_card))
            self.__resService.adding(id_res, id_film, id_card, data_time)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    @staticmethod
    def ui_bonus(card: Card):
        print("Punctele acumulate: ", card.points)

    def ui_delete_rezervare(self):
        try:
            id_res = input("Dati id-ul rezervarii de sters: ")
            self.__resService.deleting(id_res)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_modify_rezervare(self):
        try:
            id_res = input("Dati id-ul rezervarii de modificat: ")
            id_film = input("Dati id-ul filmului: ")
            id_card = input("Dati id-ul cardului clientului: ")
            data_time = datetime.strptime(
                input("Dati data si ora rezervarii:"),
                "%d.%m.%Y %H:%M")
            self.ui_in_schedule(self.__filmService.get_by_index(id_film))
            self.ui_bonus(self.__cardService.get_by_index(id_card))

            self.__resService.modify(id_res, id_film, id_card, data_time)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def show_all_rezervare(self):
        for rezervare in self.__resService.get_all():
            print(rezervare)

    def ui_in_schedule(self, film: Film):
        self.__resService.verify_schedule(film.inSchedule)

    def run_more_options(self):
        while True:
            print("1. Cautare filme si clienti. Cautare full text")
            print("2. Afișarea tuturor rezervărilor dintr-un interval de"
                  " ore dat, indiferent de zi")
            print("3. Afisarea filmelor ordonate descrescator dupa"
                  " numarul de rezervari")
            print("4. Afisarea cardurilor client ordonate descrescator"
                  " dupa numarul de puncte de pe card")
            print("5. Stergerea tuturor rezervarilor dintr-un anumit"
                  " interval de zile")
            print("6. Incrementarea cu o valoare data a punctelor de pe"
                  " toate cardurile"
                  " a caror zi de nastere se afla intr-un interval dat")
            print("x. Iesire.")
            optiune = input("Dati optiunea: ")
            if optiune == "1":
                self.ui_searching()
            elif optiune == "2":
                self.interval_de_ore()
            elif optiune == "3":
                self.ui_filme_desc()
            elif optiune == "4":
                self.ui_sort_points()
            elif optiune == "5":
                self.deleting_between_days()
            elif optiune == "6":
                self.ui_add_a_point()
            elif optiune == "x":
                print("Subprogramul se va inchide.")
                break
            else:
                print("Optiune inexistenta. Reincercati!")

    def ui_searching(self):
        given_string = input("Dati textul pe care doriti sa il cautati: ")
        for card in self.__cardService.card_searching(given_string):
            print(card)
        for film in self.__filmService.film_searching(given_string):
            print(film)

    def ui_sort_points(self):
        for card in self.__cardService.sort_by_points():
            print(card)

    def interval_de_ore(self):
        try:
            hour1 = datetime.strptime(
                input("Dati prima ora din interval:"),
                "%H:%M")
            hour2 = datetime.strptime(
                input("Dati a doua ora din interval:"),
                "%H:%M")
            for res in self.__resService.take_between_hours(hour1, hour2):
                print(res)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def ui_filme_desc(self):
        for film in self.__resService.sortingAfterRes():
            print(film)

    def deleting_between_days(self):
        day1 = datetime.strptime(
            input("Dati prima zi din interval:"),
            "%d")
        day2 = datetime.strptime(
            input("Dati a doua zi din interval:"),
            "%d")
        self.__resService.delete_between_days(day1, day2)

    def ui_add_a_point(self):
        try:
            value = int(input("Dati valoarea pentru incrementare: "))
            birthday1 = datetime.strptime(
                input("Dati prima parte a intervalului: "),
                "%d.%m.%Y")
            birthday2 = datetime.strptime(
                input("Dati a doua parte a intervalului: "),
                "%d.%m.%Y")
            self.__cardService.add_a_point(birthday1, birthday2, value)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def generare(self):
        try:
            nr_generari = int(input("Dati numarul dorit de generari: "))
            self.__filmService.random_generator(nr_generari)
        except ValueError as ve:
            print(ve)
