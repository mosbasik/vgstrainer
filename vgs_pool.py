
class Deck:
    def __init__(self):
        self.list = {}
        self.pool = []
    def new_question(self, card):
        self.list[card] = 0
    def push_pool(self, card):
        self.pool.append(card)
        self.list[card] += 1
    def pop_pool
