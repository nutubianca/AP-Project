from typing import Protocol

from Domain.entitate import Entitate


class Repository(Protocol):
    def read(self, idEntitate=None):
        ...

    def adding(self, entitate: Entitate):
        ...

    def deleting(self, idEntitate: str):
        ...

    def modify(self, entitate: Entitate):
        ...
