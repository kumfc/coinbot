import js2py as js
import core.logger as log

def generate_sign(pw):
	window = "var window = {WebSocket: 1, parseInt: parseInt, Math: Math};"
	res = js.eval_js(window + pw)
	log.debug("Generating sign: " + pw + " EQUALS " + str(res))
	return res