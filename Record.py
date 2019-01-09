class Record:
    def __init__(self, height, weight, id):
        self.__height = height
        self.__weight = weight
        self.__id = id
        self.__bmi = (float(weight)/(float(height)*float(height)))
        self.__level = ''

    def get_height(self):
        return self.__height

    def get_weight(self):
        return self.__weight

    def get_id(self):
        return self.__id

    def get_bmi(self):
        return round(self.__bmi, 2)

    def get_fitness_level(self):
        if self.__bmi < 18:
            print("Underweight, Fitness level = Unhealthy")
            self.__level = "Unhealthy"

        elif self.__bmi < 25:
            print("Normal, Fitness level = Healthy")
            self.__level = "Healthy"

        else:
            print("Overweight, Fitness level = Unhealthy")
            self.__level = "Unhealthy"

        return self.__level
