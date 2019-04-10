def init():
	global ws_handler
	global closed_ws
	global debug
	global online
	global sd_set

	ws_handler = []
	closed_ws = []
	debug = False
	online = 0
	sd_set = set()