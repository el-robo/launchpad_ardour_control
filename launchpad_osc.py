import ardour
import time
import midi_device as midi
from enum import IntEnum

class strip_button( IntEnum ):
	rec = 0,
	mute = 1,
	solo = 2

def strip_rec( id, value ):
	print( f"rec {id}:{value}" )
	midi.set_led( strip_button.rec, id, midi.color.red_full if value else midi.color.red_low )

def strip_mute( id, value ):
	print( f"mute {id}:{value}" )
	midi.set_led( strip_button.mute, id, midi.color.yellow if value else midi.color.off )

def strip_solo( id, value ):
	print( f"solo {id}:{value}" )
	midi.set_led( strip_button.solo, id, midi.color.green_full if value else midi.color.off )

def strip_count( count ):
	for row in range( count, 10 ):
		midi.clear_row( row )

ardour.strip_events = {
	"recenable": strip_rec,
	"mute": strip_mute,
	"solo": strip_solo,
	"strip_count": strip_count
}

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
