# filemon
file monitor for python based on <https://github.com/seb-m/pyinotify>

## installation
`pip install git+https://github.com/theragon/filemon.git`

## usage
```python
import filemon as fm

path_to_watch = '/dev/null'

def handle_change(evt):
	print(evt.maskname + ' detected in ' + evt.pathname)

fmon = fm.FileMon(path_to_watch, fm.IN_CLOSE_WRITE, handle_change, True)
atexit.register(goodbye, fmon)
fmon.start()
```

## things to come
*   maybe add tests
*   maybe write my own C bindings
