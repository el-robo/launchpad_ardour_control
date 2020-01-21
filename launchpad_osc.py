import ardour
import time
import midi_device

strip_list = {}

def handle_strip_event( id, verb, value ):
	print( f"strip {id} {verb}: {value}" )

def strip_list_updated( updated_strips ):
	global strip_list
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
