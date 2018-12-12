class Record:
    def __init__(self, height, weight):
        self.__height = height
        self.__weight = weight

    def get_height(self):
        return self.__height

    def get_weight(self):
        return self.__weight
