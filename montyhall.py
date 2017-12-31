
import random
import matplotlib.pyplot as plt

GOAT = 0
GOLD = 1

class Door(object):
    """
    Object to simulate a door in the monty hall game
    """
    def __init__(self, value):
        self.value = value

class MontyHall(object):
    """
    One instance of the monty hall game. Generates 3 doors and randomly
    assigns 2 doors to the value GOAT and one to GOLD.
    """
    def __init__(self):
        self.doors = [Door(GOAT), Door(GOAT),
                      Door(GOLD)]
        random.shuffle(self.doors)
        self.selection = None

    def find_door(self, value, exclude_selection=True):
        """
        Find a door that has the provided value. Exclude the
        current selection if exclude_selection is True.
        """
        for i, door in enumerate(self.doors):
            doornum = i+1
            if exclude_selection and self.selection == doornum:
                continue
            if door.value == value:
                return doornum

    def play(self, player):
        """
        Play the game with the given player.
        """
        self.selection = player.initial_choice()
        bad_door = self.find_door(GOAT)
        player.update_bad_door(bad_door)
        new_selection = player.second_choice()

        final_door = self.doors[new_selection-1]

        # Player wins if their final door selection has GOLD behind it.
        return final_door.value == GOLD


NOCHANGE = "No Change"
CHANGE = "Change"

class Player(object):
    """
    A Player that can play the monty hall game. The player is
    initialized with a strategy, CHANGE or NOCHANGE. With the CHANGE
    strategy, the player will always change their pick after the
    door with the goat is revelaed. With NOCHANGE, the player will
    always stick to its original selection.
    """
    def __init__(self, strategy):
        self.reset()
        self.strategy = strategy

    def reset(self):
        self.selection = None
        self.bad_door = None

        self.selections = set([1,2,3])

    def initial_choice(self):
        self.selection = random.randint(1,3)
        self.selections.remove(self.selection)
        return self.selection

    def update_bad_door(self, bad_door):
        self.bad_door = bad_door
        self.selections.remove(bad_door)

    def second_choice(self):
        if self.strategy == NOCHANGE:
            return self.selection
        return self.selections.pop()


def game(player):
    """
    game(player) palys one instance of the monty
    hall game with the given player
    """
    mh = MontyHall()
    return mh.play(player)

# -----------------------------------------------------------------------------------------

def test_strategy(runs, strategy):
    """
    Test a partticular strategy over a given number of runs.
    """
    success = 0
    player = Player(strategy)
    print "Running %s strategy"%strategy
    for i in xrange(runs):
        success = success + game(player)
        player.reset()
    print "Number of runs : %d\n Successes : %d, Failures : %d\n Success rate : %f" \
        % (runs, success, runs-success, float(success)/float(runs))