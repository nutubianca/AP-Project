import jsonpickle

from Domain.entitate import Entitate
from Repository.repositoryInMemory import RepositoryInMemory


class RepositoryJson(RepositoryInMemory):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __readFile(self):
        try:
            with open(self.filename, "r") as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __writeFile(self):
        with open(self.filename, "w") as f:
            f.write(jsonpickle.dumps(self.entitati))

    def read(self, idEntitate=None):
        self.entitati = self.__readFile()
        return super().read(idEntitate)

    def adding(self, entitate: Entitate):
        self.entitati = self.__readFile()
        super().adding(entitate)
        self.__writeFile()

    def deleting(self, idEntitate):
        self.entitati = self.__readFile()
        super().deleting(idEntitate)
        self.__writeFile()

    def modify(self, entitate: Entitate):
        self.entitati = self.__readFile()
        super().modify(entitate)
        self.__writeFile()
