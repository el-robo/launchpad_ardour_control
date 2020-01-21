from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm
from osc4py3 import oscbuildparse

import re
import logging

logging.basicConfig(format='%(asctime)s - %(threadName)s ø %(name)s - '
    '%(levelname)s - %(message)s')
logger = logging.getLogger( "osc" )
logger.setLevel( logging.WARNING )

update_strip_list = None
strip_event_handler = None

strip_list = None
next_strip_list = {}

def send( path, *argv ):
	msg = None

	if len( argv ):
		msg = oscbuildparse.OSCMessage( path, *argv )
	else:
		msg = oscbuildparse.OSCMessage( path, None, [] )
	osc_send( msg, "ardour" )

def process():
	osc_process()

def terminate():
	osc_terminate()

def swap_strip_list():
	
	global strip_list
	global next_strip_list
	global update_strip_list

	strip_list = next_strip_list
	next_strip_list = {}
		
	if update_strip_list:
		update_strip_list( strip_list )

def handle_strip( address, s, args ):
	
	global strip_list
	global next_strip_list
	global strip_event_handler

	match = re.match( r"^/strip/(.+)/(\d+)$", address )

	if match:
		id = match.group( 2 )
		verb = match.group( 1 )

		if strip_event_handler:
			strip_event_handler( id, verb, args[0] )
		# print( f"{id} {verb}: {args[0]}")

		if not id in next_strip_list:
			next_strip_list[ id ] = {}

		next_strip_list[ id ][ verb ] = args[ 0 ]
		

	elif address == "/strip/list":
		swap_strip_list()

def handle_reply( address, s, args ):

	global strip_list
	global next_strip_list

	if len(args) and args[ 0 ] == 'end_route_list':
		swap_strip_list()

ip = "127.0.0.1"
connect_port = 3819
listen_port = 8000

osc_startup( logger=logger )
osc_udp_server( "127.0.0.1", listen_port, "server" )
osc_udp_client( "127.0.0.1", connect_port, "ardour" )
osc_method( "/strip/*", handle_strip, argscheme=osm.OSCARG_MESSAGEUNPACK )
osc_method( "/reply", handle_reply, argscheme=osm.OSCARG_MESSAGEUNPACK )

send( "/set_surface", None, [ 0, 159, 16391, 0, 0, 0 ] )
send( "/strip/list" )

class Ardour:

	client = None
	server = None
	dispatcher = None

	def __init__(self):
		super().__init__()
		# self.dispatcher.map( "/strip/list", handle_strips, self )

	# def setup_osc(self):
		# self.client = SimpleUDPClient( self.ip, self.connect_port )
		# self.client.send_message( "/set_surface/strip_types", 1 )
		# self.client.send_message( "/set_surface", [ 0, 0, 0, 0, 0, 0 ] )

	def query_state(self):
		msg = oscbuildparse.OSCMessage( "/strip/list" )
		osc_send( msg, "ardour" )
		# self.client.send_message( "/strip/list", [] )

	# def play(self):
		# self.client.send_message( "/transport_play", [] )

	# def stop(self):
		# self.client.send_message( "/transport_stop", [] )

# async def start_server( instance, loop ):
# 	print( 'starting osc server' )

# 	dispatcher = Dispatcher()
# 	dispatcher.set_default_handler( handle_default, instance )

# 	server = AsyncIOOSCUDPServer( (instance.ip, instance.listen_port), dispatcher, asyncio.get_event_loop() )
# 	transport, protocol = await server.create_serve_endpoint()

# 	instance.setup_osc()
	
# 	await loop( instance )
	
# 	transport.close()
	
# 	print( 'closing osc server' )

# client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string