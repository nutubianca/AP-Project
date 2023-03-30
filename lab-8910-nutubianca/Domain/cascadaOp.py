from Domain.entitate import Entitate
from Domain.undoRedoOp import UndoRedoOp
from Repository.repository import Repository


class CascadaOp(UndoRedoOp):
    def __init__(self, repository1: Repository,
                 repository2: Repository,
                 object: Entitate, del_obj):
        self.__repository1 = repository1
        self.__repository2 = repository2
        self.__object = object
        self.__del_obj = del_obj

    def doUndo(self):
        self.__repository1.adding(self.__object)
        if self.__del_obj:
            for entitate in self.__del_obj:
                self.__repository2.adding(entitate)

    def doRedo(self):
        self.__repository1.deleting(self.__object.idEntitate)
        if self.__del_obj:
            for entitate in self.__del_obj:
                self.__repository2.deleting(entitate.idEntitate)
