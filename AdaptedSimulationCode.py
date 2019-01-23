import shelve


# Data for light bulbs and their wattage: 'https://www.noao.edu/education/QLTkit/ACTIVITY_Documents/Energy/TypesofLights.pdf'
class lightbulb:
    def __init__(self, type, watt, amount):
        self.__type = type
        self.__watt = watt
        self.__amount = amount

    def get_watt(self):
        return self.__watt

    def get_amount(self):
        return self.__amount


class led(lightbulb):
    def __init__(self, amount):
        super().__init__('LED', 6, amount)


class cfl(lightbulb):
    def __init__(self, amount):
        super().__init__('CFL', 9, amount)


class incandescent(lightbulb):
    def __init__(self, amount):
        super().__init__('Incandescent', 40, amount)


class toilet:
    def __init__(self, type, lpf, number):
        self.__type = type
        self.__lpf = lpf
        self.__number = number

    def get_number(self):
        return self.__number

    def get_lpf(self):
        return self.__lpf


class old(toilet):
    def __init__(self, number):
        super().__init__('Old', 10, number)


class conventional(toilet):
    def __init__(self, number):
        super().__init__('Conventional', 6, number)


class hef(toilet):
    def __init__(self, number):
        super().__init__('HEF', 4.5, number)


def calcWatt():
    with shelve.open('simStorage') as simStorage:
        ledEx = led(simStorage['ledNum'])
        cflEx = cfl(simStorage['cflNum'])
        incEx = incandescent(simStorage['incNum'])

        hrs = 8  # Assuming 8 hours used for light bulb a day

        wattLED = (ledEx.get_watt() / 1000) * hrs * 30
        wattCFL = (cflEx.get_watt() / 1000) * hrs * 30
        wattINC = (incEx.get_watt() / 1000) * hrs * 30

        amtLED = ledEx.get_amount()
        amtCFL = cflEx.get_amount()
        amtINC = incEx.get_amount()

        finalWatt = wattLED * amtLED + wattCFL * amtCFL + wattINC * amtINC
        return round(finalWatt, 3)


def calcWattPrice():
    with shelve.open('simStorage') as simStorage:
        ledEx = led(simStorage['ledNum'])
        cflEx = cfl(simStorage['cflNum'])
        incEx = incandescent(simStorage['incNum'])

        hrs = 8  # Assuming 8 hours used for light bulb a day
        cost = 0.30  # $ per kWh. Data received from 'http://energyusecalculator.com/global_electricity_prices.htm'

        calcLED = (ledEx.get_watt() / 1000) * cost * hrs * 30  #
        calcCFL = (cflEx.get_watt() / 1000) * cost * hrs * 30  # Cost per day
        calcINC = (incEx.get_watt() / 1000) * cost * hrs * 30  #

        amtLED = ledEx.get_amount()
        amtCFL = cflEx.get_amount()
        amtINC = incEx.get_amount()

        finalPrice = calcLED * amtLED + calcCFL * amtCFL + calcINC * amtINC
        return round(finalPrice, 2)


def calcCubmtr():
    with shelve.open('simStorage') as simStorage:
        toiNum = simStorage['toiletNum']
        toitype = simStorage['toiletType']
        if toitype == 'Old':
            toilet = old(toiNum)
            lpd = toilet.get_number() * toilet.get_lpf() * 24 * 6 * 30 / 1000  # 6 is the average number of times a person flushes a day
            return lpd
        elif toitype == 'Conventional':
            toilet = conventional(toiNum)
            lpd = toilet.get_number() * toilet.get_lpf() * 24 * 6 * 30 / 1000 # 6 is the average number of times a person flushes a day
            return lpd
        elif toitype == 'High Efficiency':
            toilet = hef(toiNum)
            lpd = toilet.get_number() * toilet.get_lpf() * 24 * 6 * 30 / 1000# 6 is the average number of times a person flushes a day
            return lpd


def calcCubmtrPrice():
    cubmtr = calcCubmtr()
    if cubmtr > 40:
        price = 3.69
        return price
    elif cubmtr <= 40:
        price = 2.74
        return price


def tipsElc():
    tiplist = []
    with shelve.open('simStorage') as simStorage:
        cfl = simStorage['cflNum']
        inc = simStorage['incNum']
    if inc > 0:
        tiplist.append('replaceInc')
    if cfl > 0:
        tiplist.append('replaceCfl')
    if cfl == 0 and inc == 0:
        tiplist.append('saveSmartE')
    return tiplist


def tipsWtr():
    tiplist = []
    with shelve.open('simStorage') as simStorage:
        toitype = simStorage['toiletType']
    if toitype == 'Old' or toitype == 'Conventional':
        tiplist.append('replaceOldorConv')
    else:
        tiplist.append('saveSmartW')
    return tiplist

































