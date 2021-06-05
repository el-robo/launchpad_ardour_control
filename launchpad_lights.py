#!/usr/bin/env python
import time
import midi_device as midi
from enum import IntEnum
from functools import partial

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

def handle_button( column, row, value ):

    print( f"{column}:{row}: {value}" )
    # if column in strip_handlers and value:
    if value:
        value = toggle_button_state( column, row )
        midi.set_led( column, row, value )
    
        # if value != None:
        #     strip_handlers[ column ]( row, value )

midi.cc_handler = handle_cc
midi.button_handler = handle_button

button_colors = {
    strip_button.rec: [ midi.color.red_low, midi.color.red_full ],
    strip_button.mute: [ midi.color.amber_low, midi.color.amber_full ],
    strip_button.solo: [ midi.color.green_low, midi.color.green_full ]
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
    Running = True
    print( "running" )
    
    while Running:
        time.sleep( 1 )

except KeyboardInterrupt:
    pass

finally: 
    midi.terminate()

print( 'done' )
