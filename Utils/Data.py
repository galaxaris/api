from dataclasses import dataclass

@dataclass()
class Data:
    type: str
    # serialize function get all the attributes of the class and return them as a dictionary
    def serialize(self) -> dict:
        return self.__dict__
    # deserialize function take a dictionary and set the attributes of the class
    def deserialize(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)