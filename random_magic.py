from random import randint
import copy

INIT_BLACK = 8

def random_step(vals, rows, cols, varN, grid = 1):
    return_vals = copy.deepcopy(vals)

    for r in range(rows):
        for c in range(cols):
            if return_vals[r][c] != INIT_BLACK:
                return_vals[r][c] = randint(0, varN-1)

    return return_vals