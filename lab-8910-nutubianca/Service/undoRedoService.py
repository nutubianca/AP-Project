from Domain.undoRedoOp import UndoRedoOp


class UndoRedoService:
    def __init__(self):
        self.__undoOp: list[UndoRedoOp] = []
        self.__redoOp: list[UndoRedoOp] = []

    def add_undoOp(self, undoRedoOp: UndoRedoOp):
        self.__undoOp.append(undoRedoOp)
        self.__redoOp.clear()

    def undo(self):
        if self.__undoOp:
            operation = self.__undoOp.pop()
            operation.doUndo()
            self.__redoOp.append(operation)

    def redo(self):
        if self.__redoOp:
            operation = self.__redoOp.pop()
            operation.doRedo()
            self.__undoOp.append(operation)
