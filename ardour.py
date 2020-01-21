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
strip_events = {}

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
		
	if "strip_count" in strip_events:
		strip_events[ "strip_count" ]( len( strip_list ) )

def handle_strip_event( id, verb, value ):

	if verb in strip_events:
		strip_events[ verb ]( id, value ) 

def handle_strip( address, s, args ):
	
	global strip_list
	global next_strip_list
	global strip_event_handler

	match = re.match( r"^/strip/(.+)/(\d+)$", address )

	if match:
		id = int( match.group( 2 ) ) - 1
		verb = match.group( 1 )
		handle_strip_event( id, verb, args[0] )

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

def toggle_rec():
	send( "/rec_enable_toggle" )

def start():
	send( "/transport_play" )

def stop():
	send( "/transport_stop" )

def toggle_strip_rec( strip, value ):
	send( f"/strip/recenable/{strip+1}", None, [ value ] )

def toggle_strip_mute( strip, value ):
	send( f"/strip/mute/{strip+1}", None, [ value ] )

def toggle_strip_solo( strip, value ):
	send( f"/strip/solo/{strip+1}", None, [ value ] )

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
