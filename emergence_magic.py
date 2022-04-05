
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

def emerge_step(vals, rows, cols, varN):
    
    
    pass