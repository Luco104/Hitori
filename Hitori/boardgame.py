'''
 BoardGame
 base class for board games
'''
def abstract():
    raise NotImplementedError("Abstract method")

class BoardGame:
    def play_at(self, x: int, y: int): abstract()
    def flag_at(self, x: int, y: int): abstract()
    def value_at(self, x: int, y: int) -> str: abstract()
    def cols(self) -> int: abstract()
    def rows(self) -> int: abstract()
    def finished(self) -> bool: abstract()
    def message(self) -> str: abstract()


def print_game(game: BoardGame):
    for y in range(game.rows()):
        for x in range(game.cols()):
            print('{:3}'.format(game.value_at(x, y)), end='')
        print()

def console_play(game: BoardGame):
    print_game(game)

    while not game.finished():
        x, y = input().split()
        game.play_at(int(x), int(y))
        print_game(game)

    print(game.message())
