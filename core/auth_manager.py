import websocket
import json
import time
import threading
import core.logger as log
import core.globals as g
from core.sign import generate_sign

def count_online():
	while True:
		g.online = len(g.sd_set)
		g.sd_set = set()
		time.sleep(5)

def send_click(random, sign, ws):
	time.sleep(1)
	log.debug("C10 " + str(random) + " " + str(sign))
	ws.send("C10 " + str(random) + " " + str(sign))

def ws_onmessage(ws, message):

	row = message.split()
	init = 1
	
	try:
		data = json.loads(message)
	except:
		log.debug(message)
		init = 0

	if init:
		sign = generate_sign(data['pow'])
		send_click(data['randomId'], sign, ws)
		send_click(data['randomId'], sign, ws)

	if row[0] == 'SELF_DATA':
		g.sd_set.add(g.ws_handler.index(ws))
		send_click(row[3], row[4], ws)

	elif row[0] == 'MISS':
		send_click(row[1], sign, ws)

	elif row[0] == 'ALREADY_CONNECTED':
		log.info('Подключено с другого устройства.', g.ws_handler.index(ws) + 1);

	elif row[0] == 'BROKEN':
		log.error('BROKEN ERR, SOCKET FORMAT CHANGED');

def ws_onclose(ws):
	log.info("Closed", g.ws_handler.index(ws) + 1)
	g.ws_handler.remove(ws)
	g.closed_ws.append(ws)

def ws_onerror(ws, error):
	log.debug(str(error))

def ws_onopen(ws):
	g.ws_handler.append(ws)

def ws_open(wsurl):
	#websocket.enableTrace(True)
	ws = websocket.WebSocketApp(wsurl, on_message = ws_onmessage, on_error = ws_onerror, on_close = ws_onclose, on_open = ws_onopen)
	ws.run_forever()

def ws_reload(ws):
	ws.run_forever()

def auth(db):
	for wsurl in db:
		wsopen_thread = threading.Thread(target=ws_open, args=(wsurl,))
		wsopen_thread.start()
		time.sleep(0.1)