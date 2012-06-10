"""
Program for tracking rps stats
"""


from pymongo import Connection
from bson import ObjectId

class Game(object):
    def __init__(self, player1, player2):
        self.p1 = 0
        self.player1 = player1
        self.p2 = 0
        self.player2 = player2
        self.ties = 0
        self.sequence = []
        self.id = ObjectId()

    def winner(self):
        if self.p1 >= 2:
            return self.player1
        if self.p2 >= 2:
            return self.player2
        return None

    def play(self, winner):
        if winner == self.player1:
            self.p1 += 1
        if winner == self.player2:
            self.p2 += 1
        else:
            self.ties += 1
        self.sequence.append(winner)
    def __str__(self):
        return '%s %s %s %s, %s' % (self.player1, self.p1, self.player2, self.p2, self.sequence)

class Recorder(object):
    def __init__(self, db):
        self.game_collection = db['game']
        self.play_collection = db['play']

    def record_game(self, game):
        self.game_collection.save({'_id': game.id, 'sequence': game.sequence,
                              'winner': game.winner(), game.player1: game.p1,
                              game.player2: game.p2,
                              'ties': game.ties})

    def record_play(self, game, play):
        self.play_collection.save({'game_id': game.id, 'winner': play})

if __name__ == '__main__':
    p1 = raw_input('name 1: ')
    p2 = raw_input('name 2: ')

    import curses
    scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    recorder = Recorder(Connection('localhost')['rps'])
    game = Game(p1, p2)
    plays = {'q': p1, 'w': 'tie', 'e': p2}

    while True:
        play = scr.getkey()
        scr.clear()
        scr.refresh()
        if play == 'z':
            break
        if play not in plays:
            curses.beep()
            continue
        play = plays[play]
        recorder.record_play(game, play)
        game.play(play)
        if game.winner():
            recorder.record_game(game)
            scr.addstr('Win for %s' % game.winner())
            scr.refresh()
            game = Game(p1, p2)
    curses.endwin()

    print game
