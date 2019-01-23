class Convert:
    def __init__(self, height, weight):
        self.__heightc = (float(height)/100)
        self.__weightc = (float(weight)/2.205)

    def get_heightc(self):
        return self.__heightc

    def get_weightc(self):
        return self.__weightc
