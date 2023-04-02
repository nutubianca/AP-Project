from Tests.CRUDtests import test_crud_film
from Tests.CRUDtests import test_crud_card
from Tests.CRUDtests import test_crud_reservation
from Tests.ServiceTests import test_sorting_by_points, \
    date_pentru_testare, test_sorting_after_res, \
    delete_between_days, \
    test_take_between_hours, test_film_searching, \
    test_card_searching, \
    test_add_a_point, erase_files, test_undo_redo


def all_tests():
    test_crud_film()
    test_crud_card()
    test_crud_reservation()
    date_pentru_testare()
    test_sorting_by_points()
    test_sorting_after_res()
    test_add_a_point()
    test_card_searching()
    test_film_searching()
    test_take_between_hours()
    delete_between_days()
    test_undo_redo()
    erase_files()
