
'''
Okay, let's talk this one through a little bit...

With each step, there is a certain threshold at which a sensor is liable to change its variable.

It can detect the sensors around it and what variables they are transmitting.

If the sensors around it are not transmitting a specific variable, the likelihood of changing
to that variable are high.

If the sensors are transmitting a specific variable, that decreases the likelihood that it will
change to that variable.

It can randomly change variable?

And don't forget about the edge cases

I think normalization is a necessary step, but that will take me a sec...
'''

import copy
from random import randint
import numpy as np

#Major variables
INITIAL_VAL: float = 1.0    # The array of all potential next values is initialized to _this_ value
DECREMENT_VAL: float = 1.0  # For each surrounding sensor that transmits a specific var, decrement that value _this_ much
THRESHOLD: float = 0.5      # In order for a sensor to change its var, it must pass _this_ value
STAY_BIAS: int = 0          # This is possible for the future - if we want a device to be biased toward keeping its var, fill 
                            #  in the potential array with _this_ many of that var to skew the result

# Return a list of coordinate pairs that can be accessed by this node
def getSurrounding(r, c, rows, cols, grid = 1):
    surrounding = []
    # We want to take current value into account
    surrounding.append([r,c])
    
    #If square grid, avoid the edge cases
    if grid:
        if r > 0:
            surrounding.append([r-1, c])
        if r < rows-1:
            surrounding.append([r+1, c])
        if c > 0:
            surrounding.append([r, c-1])
        if c < cols-1:
            surrounding.append([r, c+1])
    
    else:
        pass

    return surrounding

# Give back a full rows x cols array of what the next step should be
# 'grid' determines if it is hexagonal (=0) or square (=1)
def emerge_step(vals, rows, cols, varN, grid = 1):
    
    return_vals = copy.deepcopy(vals)
    
    for r in range(rows):
        for c in range(cols):
            # Start by finding out the surrounding values
            surrounding = getSurrounding(r, c, rows, cols, grid)
            # And preparing an array to be normalized
            next_vars = np.repeat(INITIAL_VAL, varN)
            
            # At this point, we have the list of surrounding squares
            #  (including the square itself, for now)
            for s in surrounding:
                next_vars[vals[s[0]][s[1]]] -= DECREMENT_VAL

            # We have now taken all values into account, we need to normalize
            # If all values are equal, do this explicitly to avoid dividng by 0
            if next_vars.max() == next_vars.min():
                next_norm = np.repeat(1.0, varN)
            else:
                next_norm = (next_vars - next_vars.min()) / (next_vars.max() - next_vars.min())
            
            # Now we generate the indices that surpassed the threshold
            next_possible = []
            for i in range(varN):
                if next_norm[i] > THRESHOLD:
                    next_possible.append(i)
                
            # Add a bias to stay on the same value    
            for i in range(STAY_BIAS):
                next_possible.append(vals[r][c])

            # Randomly select a value from the next_possible array
            next_sure = next_possible[randint(0, len(next_possible)-1)]

            # Save this as our final decision
            return_vals[r][c] = next_sure

    return return_vals
            

    
    