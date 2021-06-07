from state import State
from midi_device import color
from copy import copy

def poll_generators( state, generators ):
    i = 0
    while i < len(generators):
        try:
            gen_state = next( generators[ i ] )
            state.merge( gen_state )
            i+=1            
        except StopIteration:
            del generators[ i ]

def run_down( button, value ):
    state = State()

    while True:
        state.set( button, color.off )
        button.x += 1

        if button.x >= button.max_x:
            button.x = 0
            button.y += 1

            if button.y >= button.max_y:
                break

        state.set( button, value )
        yield state

def direction( button, value, x, y ):
    state = State()
    
    button = copy( button )
    while True:
        state.set( button, color.off )
        button.x = button.x + x
        button.y = button.y + y

        if not button.in_range():
            break

        state.set( button, value )
        yield state

def cross( button, value ):
    
    generators = [
        direction( button, value, -1, 0 ),
        direction( button, value, 1, 0 ),
        direction( button, value, 0, -1 ),
        direction( button, value, 0, 1 )
    ]

    state = State()

    while len( generators ):
        state.fill( color.off )
        poll_generators( state, generators )
        yield state


def star( button, value ):
    
    generators = [
        direction( button, value, -1, 0 ),
        direction( button, value, 1, 0 ),
        direction( button, value, 0, -1 ),
        direction( button, value, 0, 1 ),

        direction( button, value, -1, 1 ),
        direction( button, value, -1, -1 ),
        direction( button, value, 1, -1 ),
        direction( button, value, 1, 1 )
    ]

    state = State()

    while len( generators ):
        state.fill( color.off )
        poll_generators( state, generators )
        yield state