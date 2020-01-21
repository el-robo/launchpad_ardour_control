import ardour
import time
import midi_device as midi
from enum import IntEnum

class cc_button( IntEnum ):
	rec = 0,
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
		return None
	else:
		button_state[ key ] = 1 - button_state[ key ]

	return button_state[ key ]

#####################
# midi event handlers

cc_handlers = {
	int( cc_button.rec ): ardour.toggle_rec,
	int( cc_button.stop ): ardour.stop,
	int( cc_button.start ): ardour.start
}

def handle_cc( column, value ):

	if column in cc_handlers and value:
		cc_handlers[ column ]()

strip_handlers = {
	int( strip_button.rec ): ardour.toggle_strip_rec,
	int( strip_button.mute ): ardour.toggle_strip_mute,
	int( strip_button.solo ): ardour.toggle_strip_solo
}

def handle_button( column, row, value ):

	if column in strip_handlers and value:
		value = toggle_button_state( column, row )

		if value != None:
			strip_handlers[ column ]( row, value )

midi.cc_handler = handle_cc
midi.button_handler = handle_button

#######################
# ardour event handlers

def rec( value ):
	store_cc_state( cc_button.rec, value )
	midd.set

def strip_rec( id, value ):
	store_button_state( strip_button.rec, id, value )
	midi.set_led( strip_button.rec, id, midi.color.red_full if value else midi.color.red_low )

def strip_mute( id, value ):
	store_button_state( strip_button.mute, id, value )
	midi.set_led( strip_button.mute, id, midi.color.yellow if value else midi.color.off )

def strip_solo( id, value ):
	store_button_state( strip_button.solo, id, value )
	midi.set_led( strip_button.solo, id, midi.color.green_full if value else midi.color.off )

def strip_count( count ):

	for row in range( count, 10 ):
		midi.clear_row( row )
		
		for column in range( 10 ):
			key = (column,row)
			if key in button_state: 
				del( button_state[ key ] )

ardour.strip_events = {
	"recenable": strip_rec,
	"mute": strip_mute,
	"solo": strip_solo,
	"strip_count": strip_count
}

#################
# main event loop

try:
	Running = True

	while Running:
		ardour.process()

except KeyboardInterrupt:
	pass

finally: 
	ardour.terminate()
	midi.terminate()

print( 'done' )
