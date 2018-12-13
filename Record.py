import datetime


class Record:
    def __init__(self, height, weight, id):
        self.__height = height
        self.__weight = weight
        self.__id = id

    def get_height(self):
        return self.__height

    def get_weight(self):
        return self.__weight

    def get_id(self):
        return self.__id
