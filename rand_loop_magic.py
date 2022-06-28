import copy

INIT_BLACK = 8

def rand_loop_step(vals, rows, cols, varN, grid = 1):
    return_vals = copy.deepcopy(vals)

    for r in range(rows):
        for c in range(cols):
            if return_vals[r][c] != INIT_BLACK:
                return_vals[r][c] = (return_vals[r][c] + 1) % varN

    return return_vals