import ardour
import time
import midi_device as midi
from enum import IntEnum

strips = {}

class strip_button( IntEnum ):
	rec = 0,
	mute = 1

def toggle_strip_rec( id, value ):
	print( f"rec {id}:{value}" )
	midi.set_led( strip_button.rec, id, midi.color.red_full if value else midi.color.red_low )

def mute_strip( id, value ):
	print( f"mute {id}:{value}" )
	midi.set_led( strip_button.mute, id, midi.color.red_full if value else midi.color.red_low )

ardour_events = {
	"recenable": toggle_strip_rec,
	"mute": mute_strip
}

def handle_strip_event( id, verb, value ):
	print( f"strip {id} {verb}: {value}" )

	if verb in ardour_events:
		ardour_events[ verb ]( id, value ) 

def clear_row( row ):
	print( f"clearing row {row}" )
	
	for i in range( 9 ):
		midi.set_led( i, row, midi.color.off )

def strip_list_updated( updated_strips ):
	global strips

	if len( strips ) > len( updated_strips ):
		# clear excess rows
		for row in range( len( updated_strips ), len( strips ) ):
			clear_row( row )

	strips = updated_strips
	print( "strips updated" )
	
	for i in range( 1, len( strips ) + 1  ):
		key = f"{i}"
		# print( f"strip {i}: {strips[key]['name']}" )

try:
	for row in range( 10 ):
		clear_row( row ) 

	ardour.update_strip_list = strip_list_updated
	ardour.strip_event_handler = handle_strip_event

	Running = True

	while Running:
		ardour.process()

except KeyboardInterrupt:
	pass

finally: 
	ardour.terminate()
	midi.terminate()

print( 'done' )
