# utf8
# Yili Lin 6/22/2020
import os
import sys
import random
import itertools


def trim(seq, direction=0):
    '''
    direction = 0 for left, 1 for right
    [0,2,2,0]
    left:[2,2] +[0,0,0,0] = [2,2,0,0,0,0][:4]
    right:[0,0,0,0]+[2,2] = [0,0,0,0,2,2][-4:]
    '''
    if direction:  # right
        return ([0, 0, 0, 0] + [n for n in seq if n])[-4:]
    else:  # left
        return ([n for n in seq if n] + [0, 0, 0, 0])[:4]


def sum_seq(seq, direction=0):
    '''
    get sum for the sequence
    [0,1],[1,2],[2,3] for example[0,2,2,4] to [0,0,4,4]
    [1,2]
        :return
    [0,1], [2,3]
        compare
    '''
    if seq[1] and seq[2] and seq[1] == seq[2]:  # [1,2] the same
        return trim([seq[0], seq[1] * 2, 0, seq[3]], direction=direction)
    if seq[0] and seq[1] and seq[0] == seq[1]:  # [0,1] the same
        seq[0], seq[1] = seq[0] * 2, 0
    if seq[2] and seq[3] and seq[2] == seq[3]:  # [2,3] the same
        seq[2], seq[3] = seq[2] * 2, 0
    return trim(seq, direction=direction)


def up(grid):
    '''control move up control command w'''
    for col in [0, 1, 2, 3]:
        for index, n in enumerate(sum_seq(trim([row[col] for row in grid]))):
            grid[index][col] = n
    return grid


def down(grid):
    '''control move down control command d'''
    for col in [0, 1, 2, 3]:
        for index, n in enumerate(sum_seq(trim([row[col] for row in grid], direction=1), direction=1)):
            grid[index][col] = n
    return grid


def left(grid):
    '''control move left control command a'''
    return [sum_seq(trim(row)) for row in grid]


def right(grid):
    '''control move right control command d'''
    return [sum_seq(trim(row, direction=1), direction=1) for row in grid]


class Game:
    '''main game class'''
    gride = []
    conrtrols = ['w', 'a', 's', 'd']  # use w,a,s,d to control the game

    def rnd_num(self):
        '''generate the initial 2 or 4'''
        num = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4])  # more chance to get a 2 than 4
        x, y = random.choice([(x, y) for x, y in itertools.product([0, 1, 2, 3], [0, 1, 2, 3]) if self.grid[x][y] == 0])
        self.grid[x][y] = num

    def print_screen(self):
        '''draw the game picture'''
        os.system('cls')  # clean for game window use 'clear' for mac
        print('-' * 21)
        for row in self.grid:
            print(f"|{'|'.join([str(col or ' ').center(4) for col in row])}|")
            print('-' * 21)

    def logic(self, control):
        '''control for the game
        1 for win
        -1 for lose'''
        controls = {'w': up, 's': down, 'a': left, 'd': right}
        grid = controls[control.lower()]([[col for col in row] for row in self.grid])
        if grid != self.grid:
            del self.grid[:]
            self.grid.extend(grid)
            if [num for num in itertools.chain(*grid) if num >= 2048]:  # the winning conditions
                return 1, "You win!"
            self.rnd_num()  # not win add a new 2 or 4 to the grid
        else:
            if not [1 for g in [c(grid) for c in [up, down, left, right]] if g != self.grid]:
                return -1, "You lose."
        return 0, ''

    def game_play(self):
        '''main loop for the game'''
        self.grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # initial the grid
        self.rnd_num()  # add two random 2 or 4 to the grid
        self.rnd_num()
        while True:
            self.print_screen()
            control = input('input w/a/s/d')
            if control.lower() in self.conrtrols:
                status, info = self.logic(control)
                if status:
                    print(info)
                    if input('New game? [Y/N]').lower() == 'y':
                        break
                    else:
                        sys.exit(0)
        self.main()


if __name__ == "__main__":
    Game().game_play()
