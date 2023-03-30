from Domain.entitate import Entitate
from Domain.undoRedoOp import UndoRedoOp
from Repository.repository import Repository


class AddOp(UndoRedoOp):
    def __init__(self, repository: Repository,
                 addedObj: Entitate):
        self.__repository = repository
        self.__addedObj = addedObj

    def doUndo(self):
        self.__repository.deleting(
            self.__addedObj.idEntitate)

    def doRedo(self):
        self.__repository.adding(self.__addedObj)
