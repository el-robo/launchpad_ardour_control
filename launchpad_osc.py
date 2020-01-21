import ardour
import time
import midi_device as midi

strips = {}

def mute_strip( id, value ):
	print( f"mute {id}" )

events = {
	"mute": mute_strip
}

def handle_strip_event( id, verb, value ):
	print( f"strip {id} {verb}: {value}" )

	if verb in events:
		events[ verb ]( id, value ) 
	# midi.set_led

def clear_row( row ):
	print( f"clearing row {row}" )

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
	ardour.update_strip_list = strip_list_updated
	ardour.strip_event_handler = handle_strip_event

	Running = True

	while Running:
		ardour.process()

except KeyboardInterrupt:
	pass

finally: 
	ardour.terminate()
	midi_device.terminate()

print( 'done' )
# 	print( 'done' )
