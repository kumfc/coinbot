import threading
import time
import core.auth_manager as auth_manager
import core.logger as log
import core.globals as g

db = []

def loop():
	while True:
		log.puts('Bots online: ' + str(g.online))
		log.puts('Choose what to do:')
		log.puts('1 - Reconnect All')
		log.puts('2 - Count opened WebSockets')
		log.puts('3 - Count closed WebSockets')
		try:
			ch = int(input())
		except:
			continue
		if ch == 1:
			for ws in g.closed_ws:
				g.closed_ws.remove(ws)
				ws_loop = threading.Thread(target=auth_manager.ws_reload, args=(ws,))
				ws_loop.start()
		elif ch == 2:
			log.puts("WebSockets opened: " + str(len(g.ws_handler)))
		elif ch == 3:
			log.puts("WebSockets closed: " + str(len(g.closed_ws)))
		time.sleep(1)


def main():
	g.init()

	with open('db.txt') as f:
		for line in f:
			line = line.replace('\n', '')
			db.append(line)
	log.info("Parsed " + str(len(db)) + " accounts")

	auth_thread = threading.Thread(target=auth_manager.auth, args=(db,))
	auth_thread.start()
	online_loop = threading.Thread(target=auth_manager.count_online)
	online_loop.start()
	menu_loop = threading.Thread(target=loop)
	menu_loop.start()

if __name__ == "__main__":
    main()