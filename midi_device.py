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

input = rtmidi.MidiIn()
ports = input.get_ports()

for idx,key in enumerate( ports ):
	print( key )

matching_port = [ idx for idx,key in enumerate( ports ) if key.startswith( 'Launchpad' ) ]

if len( matching_port ) == 0:
	raise Exception( 'no Launchpad device found' )

input.open_port( matching_port[0] )
input.set_callback( MidiInputHandler( 'launchpad' ) )

def terminate():
	global input
	input.close_port()
	del input