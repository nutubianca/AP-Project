from abc import ABC


class UndoRedoOp(ABC):
    def doUndo(self):
        ...

    def doRedo(self):
        ...
