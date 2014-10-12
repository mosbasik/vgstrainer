
class Card:

    def __init__(self, front, back):
        '''
        Card class constructor
        '''
        self.front = front
        self.back = back
        self.id = hash((front, back))

    def __hash__(self):
        '''
        Signals immutability.  Allows the use of Card as a key in dictionaries,
        sets, etc
        '''
        return hash((self.front, self.back))

    def __eq__(self):
        '''
        Allows membership testing when used in lists
        '''
        if isinstance(other, self.__class__):
            return self.id == other.id
        return NotImplemented

    def get_front(self):
        return self.front

    def get_back(self):
        return self.back

    def get_id(self):
        return self.id



class Deck:
    def __init__(self):
        '''
        Deck class constructor
        '''
        self.deck = {}

    def put_card(self, card):
        '''
        Add a new question card to the deck
        '''
        self.deck[card] = 0



class Pool:
    def __init__(self):
        '''
        Pool class constructor
        '''
        self.pool = []

    def put_card(self, card)