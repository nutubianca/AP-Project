from Domain.entitate import Entitate
from Domain.undoRedoOp import UndoRedoOp
from Repository.repository import Repository


class ModifyOp(UndoRedoOp):
    def __init__(self, repository: Repository,
                 new_obj: Entitate,
                 old_obj: Entitate):
        self.__repository = repository
        self.__new_obj = new_obj
        self.__old_obj = old_obj

    def doUndo(self):
        self.__repository.modify(self.__old_obj)

    def doRedo(self):
        self.__repository.modify(self.__new_obj)
