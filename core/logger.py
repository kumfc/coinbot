import datetime
import core.globals as g

def ts():
	return str(datetime.datetime.now().strftime("%I:%M:%S"))

def error(text):
	print("[" + ts() + "][!] " + str(text))

def info(text, ws = 0):
	if ws != 0:
		print("[" + ts() + "][*][WebSocket " + str(ws) + "] " + str(text))
	else:
		print("[" + ts() + "][*] " + str(text))

def puts(text):
	print("[*] " + str(text))

def debug(text):
	if not g.debug:
		return
	print("[DEBUG] " + str(text))

def donothing(text):
	return