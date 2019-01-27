class Record:
    def __init__(self, height, weight, date):
        self.__height = height
        self.__weight = weight
        self.__bmi = (float(weight)/(float(height)*float(height)))
        self.__level = ''
        self.__date = date

    def get_date(self):
        return self.__date

    def get_height(self):
        return self.__height

    def get_weight(self):
        return self.__weight

    def get_bmi(self):
        return round(self.__bmi, 2)

    def get_fitness_level(self):
        if self.__bmi < 18:
            print("Underweight, Fitness level = Unhealthy")
            self.__level = "Underweight, Unhealthy"

        elif self.__bmi < 25:
            print("Normal, Fitness level = Healthy")
            self.__level = "Normal, Healthy"

        else:
            print("Overweight, Fitness level = Unhealthy")
            self.__level = "Overweight, Unhealthy"

        return self.__level
