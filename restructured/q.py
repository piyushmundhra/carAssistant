class Qgoog():
    name = 'Qgoog'
    hotwords = []

    def process(self, sentence):
        return 'Searching Google'

class Qmap():
    name = 'Qmap'
    hotwords = ['street', 'intersection']

    def process(self, sentence):
        return 'Searching Maps'

class Qcar():
    name = 'Qcar'
    hotwords = ['lock', 'door', 'window', 'seatbelt']

    def process(self, sentence):
        return 'Let me check the car condition'
