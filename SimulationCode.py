# Light bulb classes below
# Data for light bulbs and their wattage: 'https://www.noao.edu/education/QLTkit/ACTIVITY_Documents/Energy/TypesofLights.pdf'
class lightbulb:
    def __init__(self, type, watt):
        self.__type = type
        self.__watt = watt

    def get_type(self):
        return self.__type

    def get_watt(self):
        return self.__watt

    def set_watt(self, watt):
        self.__watt = watt

    def set_type(self, type):
        self.__type = type

    def __str__(self):
        pass

# LED light bulb
class led(lightbulb):
    def __init__(self):
        super().__init__('LED', 6)

    def __str__(self):
        return 'LED'

# CFL light bulb
class cfl(lightbulb):
    def __init__(self):
        super().__init__('CFL', 9)

    def __str__(self):
        return 'CFL'

# Incandescent light bulb
class incandescent(lightbulb):
    def __init__(self):
        super().__init__('Incandescent', 40)

    def __str__(self):
        return 'Incandescent'
# End of classes

# Main simulation function
def main():

    # Function to calculate price
    def calcPrice():
        ledEx = led()
        cflEx = cfl()
        incEx = incandescent()

        hrs = 8  # Assuming 8 hours used for light bulb a day
        cost = 0.30  # $ per kWh. Data received from 'http://energyusecalculator.com/global_electricity_prices.htm'

        calcLED = (ledEx.get_watt() / 1000) * cost * hrs  #
        calcCFL = (cflEx.get_watt() / 1000) * cost * hrs  # Cost per day
        calcINC = (incEx.get_watt() / 1000) * cost * hrs  #

        finalPrice = calcLED * len(leds) + calcCFL * len(cfls) + calcINC * len(inc)
        return finalPrice

    leds = []
    cfls = []
    inc = []
    choose = int(input('How many light bulbs do you have at home? '))
    option = int(input('How many of them are LED, CFL or Incandescent light bulbs? (Enter a number)' 
            '\n1. All are LEDs' 
            '\n2. All are CFLs' 
            '\n3. All are Incandescent'
            '\n4. Custom ' ))

    if option == 1:
        for i in range(choose):
            name = led()
            leds.append(name)
        print('You have %d LED light bulbs.' %(len(leds)))

    elif option == 2:
        for i in range(choose):
            name = cfl()
            cfls.append(name)
        print('You have %d CFL light bulbs.' %(len(cfls)))

    elif option == 3:
        for i in range(choose):
            name = incandescent()
            inc.append(name)
        print('You have %d Incandescent light bulbs.' %(len(inc)))

    elif option == 4:
        ledCount = int(input('How many LED light bulbs do you have? '))
        if ledCount <= choose:
            for i in range(ledCount):
                name = led()
                leds.append(name)

            newchoose = choose - ledCount
            cflCount = int(input('How many CFL light bulbs do you have? '))
            if cflCount <= newchoose:
                for i in range(cflCount):
                    namae = cfl()
                    cfls.append(namae)

                newerchoose = newchoose - cflCount
                incCount = int(input('How many Incandescent light bulbs do you have? '))
                if incCount <= newerchoose:
                    for i in range(incCount):
                        nama = incandescent()
                        inc.append(nama)

        print('In total, you have %d LED, %d CFL and %d Incandescent light bulbs.' %(len(leds), len(cfls), len(inc)))
    print('You spend ${:.2f} per day, assuming 8 hours of daily usage and $0.30 cost per kWh.' .format(calcPrice()))


main()














































