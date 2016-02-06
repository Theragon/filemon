import filemon as fm
import atexit
import time
import sys

path = sys.argv[1]


def goodbye(fmon):
	fmon.stop()


def handle_change(evt):
	print(evt.maskname + ' detected in ' + evt.pathname)

fmon = fm.FileMon(path, fm.ALL_EVENTS, handle_change, True)
atexit.register(goodbye, fmon)
fmon.start()

while True:
	time.sleep(1)
