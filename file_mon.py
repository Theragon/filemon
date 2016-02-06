import test_config as cfg
import pyinotify
import asyncore
import atexit
import time
#import os
from pyinotify import IN_ACCESS
from pyinotify import IN_ATTRIB
from pyinotify import IN_CLOSE_NOWRITE
from pyinotify import IN_CLOSE_WRITE
from pyinotify import IN_CREATE
from pyinotify import IN_DELETE
from pyinotify import IN_DELETE_SELF
from pyinotify import IN_DONT_FOLLOW
from pyinotify import IN_IGNORED
from pyinotify import IN_ISDIR
from pyinotify import IN_MASK_ADD
from pyinotify import IN_MODIFY
from pyinotify import IN_MOVE_SELF
from pyinotify import IN_MOVED_FROM
from pyinotify import IN_MOVED_TO
from pyinotify import IN_ONLYDIR
from pyinotify import IN_OPEN
from pyinotify import IN_Q_OVERFLOW
from pyinotify import IN_UNMOUNT


def goodbye(fm):
	fm.stop()


class ModHandler(pyinotify.ProcessEvent):
	"""ModHandler class reloads config when a change is detected"""
	def __init__(s, mask, callback):
		s.mask = mask
		s.callback = callback

	def process_default(s, evt):
		s.callback(evt)

	"""def process_IN_CLOSE_WRITE(self, evt):
					#global test_config
					print('Config file changed, reloading config: ' + evt.pathname)
					print('before reload: ' + str(cfg.port))
					reload(cfg)
					print('after reload: ' + str(cfg.port))"""


class FileMon():
	"""docstring for FileMon"""
	def callback(s, evt):
		print(evt.maskname + ' detected in ' + evt.pathname)

	def __init__(s, path, event_types, threaded=True):
		if threaded:
			s.threaded = True
		else:
			s.asyncr = True
		try:
			mask = 0
			for t in event_types:
				mask |= t
		except TypeError:
			mask = mask | event_types
		s.handler = ModHandler(mask, s.callback)
		s.wm = pyinotify.WatchManager()
		if s.threaded:
			s.notifier = pyinotify.ThreadedNotifier(s.wm, s.handler)
		else:
			s.notifier = pyinotify.AsyncNotifier(s.wm, s.handler)
		s.wdd = s.wm.add_watch(path, mask)

	def start(s):
		if s.threaded:
			s.notifier.setDaemon(True)
			s.notifier.start()
		else:
			asyncore.loop()

	def stop(s):
		print("File monitor shutting down")
		if s.threaded:
			s.notifier.stop()
		else:
			raise asyncore.ExitNow()


def main():
	print('on start: ' + str(cfg.port))
	fm = FileMon('test_config.py', IN_CLOSE_WRITE, True)
	atexit.register(goodbye, fm)
	fm.start()

	while True:
		time.sleep(1)

if __name__ == '__main__':
	main()
