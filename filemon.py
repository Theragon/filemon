#import test_config as cfg
import pyinotify
import asyncore
#import atexit
#import time
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

ALL_EVENTS = [
	IN_ACCESS,
	IN_ATTRIB,
	IN_CLOSE_NOWRITE,
	IN_CLOSE_WRITE,
	IN_CREATE,
	IN_DELETE,
	IN_DELETE_SELF,
	IN_DONT_FOLLOW,
	IN_IGNORED,
	IN_ISDIR,
	IN_MASK_ADD,
	IN_MODIFY,
	IN_MOVE_SELF,
	IN_MOVED_FROM,
	IN_MOVED_TO,
	IN_ONLYDIR,
	IN_OPEN,
	IN_Q_OVERFLOW,
	IN_UNMOUNT,
]


class ModHandler(pyinotify.ProcessEvent):
	"""ModHandler class reloads config when a change is detected"""
	def __init__(s, mask, callback):
		s.mask = mask
		s.callback = callback

	def process_default(s, evt):
		s.callback(evt)


class FileMon():
	"""docstring for FileMon"""
	def do_callback(s, evt):
		s.callback(evt)

	def __init__(s, path, event_types, callback, threaded=True):
		s.callback = callback
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
		s.handler = ModHandler(mask, s.do_callback)
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
