import rtmidi
import logging
import sys
import math
import time
from enum import IntEnum

button_handler = None
cc_handler = None

input = rtmidi.MidiIn()
output = rtmidi.MidiOut()

def handle_button( index, value ):
    column = index % 0x10
    row = math.floor( (index - column) / 0x10 )

    if button_handler:
        button_handler( column, row, value )

def handle_cc( index, value ):
    column = index - 104

    if cc_handler:
        cc_handler( column, value )

midi_handlers = {
    144: handle_button,
    176: handle_cc
}

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        print( "init" )

    def __call__( self, event, data=None ):
        message, deltatime = event

        if message[ 0 ] in midi_handlers:
            midi_handlers[ message[ 0 ] ]( message[ 1 ], min( 1, message[ 2 ] ) )

def open_launchpad( device ):
    ports = device.get_ports()

    matching_port = [ idx for idx,key in enumerate( ports ) if key.startswith( 'Launchpad' ) ]

    if len( matching_port ) == 0:
        raise Exception( 'no Launchpad input device found' )

    device.open_port( matching_port[0] )

def start():
    print( "opening device" )
    open_launchpad( input )
    open_launchpad( output )
    input.set_callback( MidiInputHandler( 'launchpad' ) )

class color( IntEnum ):
    off 			= 0x0C,
    red_low 		= 0x0D,
    red_full 		= 0x0F,
    red_flash		= 0x0B,
    amber_low		= 0x1D,
    amber_full		= 0x3F,
    amber_flash		= 0x3B,
    yellow			= 0x3E,
    yellow_flash 	= 0x3A,
    green_low		= 0x1C,
    green_full		= 0x3C,
    green_flash		= 0x38

def terminate():
    global input
    input.close_port()
    del input

    global output
    output.close_port()
    del output    

def set_led( column, row, value ):
    global output

    command = [ 0x90, 0x10 * int(row) + int(column), int(value) ]
    output.send_message( command )

def clear_row( row ):
    
    for i in range( 9 ):
        set_led( i, row, color.off )

def reset():
    global output
    output.send_message( [ 0xB0, 0x00, 0x00 ] )