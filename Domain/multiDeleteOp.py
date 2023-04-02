from Domain.undoRedoOp import UndoRedoOp
from Repository.repository import Repository


class MultiDeleteOp(UndoRedoOp):
    def __init__(self, repository: Repository, del_obj):
        self.repository = repository
        self.__del_obj = del_obj

    def doUndo(self):
        for entitate in self.__del_obj:
            self.repository.adding(entitate)

    def doRedo(self):
        for entitate in self.__del_obj:
            self.repository.deleting(entitate.idEntitate)
