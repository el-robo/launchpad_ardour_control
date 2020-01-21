import rtmidi
import logging
import sys
import time

class MidiInputHandler(object):
	def __init__(self, port):
		self.port = port
		self._wallclock = time.time()

	def __call__(self, event, data=None):
		message, deltatime = event
		self._wallclock += deltatime
		print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))

def open_launchpad( device ):
	ports = device.get_ports()

	for idx,key in enumerate( ports ):
		print( key )

	matching_port = [ idx for idx,key in enumerate( ports ) if key.startswith( 'Launchpad' ) ]

	if len( matching_port ) == 0:
		raise Exception( 'no Launchpad input device found' )

	device.open_port( matching_port[0] )

input = rtmidi.MidiIn()
output = rtmidi.MidiOut()

open_launchpad( input )
open_launchpad( output )

input.set_callback( MidiInputHandler( 'launchpad' ) )

def terminate():
	global input
	input.close_port()
	del input

def set_led( column, row, value ):
	global output
	output.send_message( [ 0x90, 0x10 * row + column, value ] )

set_led( 0, 0, 0x0D )