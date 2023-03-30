from Domain.entitate import Entitate
from Domain.undoRedoOp import UndoRedoOp
from Repository.repository import Repository


class DeleteOp(UndoRedoOp):
    def __init__(self, repository: Repository,
                 deleted_obj: Entitate):
        self.__repository = repository
        self.__deleted_obj = deleted_obj

    def doUndo(self):
        self.__repository.adding(self.__deleted_obj)

    def doRedo(self):
        self.__repository.deleting(
            self.__deleted_obj.idEntitate)
