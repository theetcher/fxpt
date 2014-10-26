import sys
import os


scriptDir = os.path.dirname(__file__).replace('\\', '/')
dirs = scriptDir.split('/')
fxptLocation = '/'.join(dirs[:-3])

if not fxptLocation in sys.path:
    sys.path.append(fxptLocation)
