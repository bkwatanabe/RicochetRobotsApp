from board import board_factory
import uuid

class Game:
    def __init__(self, board = None):
        self.id = str(uuid.uuid1())
        self.players = set()
        self.board = board
        if board == None:
            self.board = board_factory()
        print("id", self.id)

