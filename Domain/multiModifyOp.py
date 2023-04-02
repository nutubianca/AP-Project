from Domain.undoRedoOp import UndoRedoOp
from Repository.repository import Repository


class MultiModifyOp(UndoRedoOp):
    def __init__(self, repository: Repository, new_obj, old_obj):
        self.repository = repository
        self.__new_obj = new_obj
        self.__old_obj = old_obj

    def doUndo(self):
        for entitate in self.__old_obj:
            self.repository.modify(entitate)

    def doRedo(self):
        for entitate in self.__new_obj:
            self.repository.modify(entitate)
