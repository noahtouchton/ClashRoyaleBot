


class Card():
    def __init__(self, name: str, id: int, elixer_cost: int):
        self.name = name
        self.id = id
        self.elixer = elixer_cost


    def get_id(self) -> int:
        return self.id
    def get_elixer(self) -> int:
        return self.elixer

class Player:
    def __init__(self, deck: list[int], hand: list[int], next: int, elixer: float):
        self.deck = deck
        self.hand = hand
        self.next = next
        self.elixer = elixer


class Troop():
    def __init__(self, card: Card, pos_x: int, pos_y: int):
        self.card = card
        self.pos_x = pos_x
        self.pos_y = pos_y


class State:
    def __init__(self, minutes: int, seconds: int, player_troops: list[Troop], enemy_troops: list[Troop], overtime: bool = False):
        self.overtime = overtime
        self.minutes = minutes
        self.seconds = seconds
        self.player_troops = player_troops
        self.enemy_troops = enemy_troops

    def get_time_remaining(self) -> int:
        return self.minutes * 60 + self.seconds