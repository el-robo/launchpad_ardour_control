#!/usr/bin/env python
from button import Button
from state import State
import effects
import time
import midi_device as midi
from midi_device import color
from enum import IntEnum
import random
class cc_button( IntEnum ):
    rec = 0,
    click = 1,
    stop = 2,
    start = 3

class strip_button( IntEnum ):
    rec = 0,
    mute = 1,
    solo = 2

current_strip_count = 0
button_state = {}

def store_button_state( column, row, value ):
    button_state[ (int(column), int(row)) ] = value

def toggle_button_state( column, row ):

    key = (column,row)

    if key not in button_state:
        button_state[ key ] = 1
    else:
        button_state[ key ] = 1 - button_state[ key ]

    return button_state[ key ]

#####################
# midi event handlers

generators = []

cc_handlers = {
    # int( cc_button.rec ): ardour.toggle_rec,
    # int( cc_button.click ): ardour.toggle_click,
    # int( cc_button.stop ): ardour.stop,
    # int( cc_button.start ): ardour.start
}

def handle_cc( column, value ):

    print( f"{column}: {value}" )
    if column in cc_handlers and value:
        cc_handlers[ column ]()

main_colors = [ color.red_full, color.amber_full, color.green_full, color.yellow ]

def random_color():
    return main_colors[ random.randint( 0, len( main_colors ) - 1 ) ]

def handle_button( column, row, value ):

    print( f"{column}:{row}: {value}" )

    button = Button( column, row )
    color = random_color()

    if value:
        # generators.append( effects.run_down( Button( column, row ) ) )
        # generators.append( effects.direction( button, 1, 0 ) )
        # generators.append( effects.cross( button ) )

        generators.append( effects.star( button, color ) )
        # value = toggle_button_state( column, row )
        # midi.set_led( column, row, value )
    
midi.cc_handler = handle_cc
midi.button_handler = handle_button

button_colors = {
    strip_button.rec: [ color.red_low, color.red_full ],
    strip_button.mute: [ color.amber_low, color.amber_full ],
    strip_button.solo: [ color.green_low, color.green_full ]
}

def set_strip_led( type, id, value ):
    store_button_state( type, id, value )
    midi.set_led( type, id, button_colors[ type ][ 1 ] if value else button_colors[ type ][ 0 ] )

def strip_count( count ):

    for row in range( count, 10 ):
        midi.clear_row( row )
        
        for column in range( 10 ):
            key = (column,row)
            if key in button_state: 
                del( button_state[ key ] )
#################
# main event loop
try:
    midi.start()
    time.sleep( 0.1 )

    midi.reset()
    time.sleep( 0.1 )

    Running = True
    print( "running" )
    current_state = State()
    state = State()

    while Running:
        state.fill( color.off )
        effects.poll_generators( state, generators )
        current_state.apply( state )
        time.sleep( 0.06 )

except KeyboardInterrupt:
    pass

midi.terminate()
print( 'done' )
