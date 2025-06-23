import abc

class Service(abc.ABC):
    def __init__(self, **kwargs) -> None:
        for name, repository in kwargs.items():
            setattr(self, name, repository)