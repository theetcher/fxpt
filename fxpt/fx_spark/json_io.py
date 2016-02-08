import os
import json

from fxpt.fx_utils.message_box import messageBox
from fxpt.fx_utils.utils import makeWritable


def load(filename, silent=False):
    try:
        with open(filename, 'r') as f:
            obj = json.load(f)
    except IOError:
        if not silent:
            if not os.path.exists(filename):
                messageBox(text='Cannot load .json file. File does not exists:\n{}'.format(filename))
            else:
                messageBox(text='Cannot load .json file:\n{}'.format(filename))
        raise
    except ValueError:
        if not silent:
            messageBox(text='Error parsing .json file. Check syntax:\n{}'.format(filename))
        raise
    except StandardError:
        if not silent:
            messageBox(text='Unexpected error loading .json file:\n{}'.format(filename))
        raise

    return obj


def dump(filename, obj, silent=False):
    try:
        makeWritable(filename)
        with open(filename, 'w') as f:
            obj = json.dump(obj, f, sort_keys=True, indent=4, separators=(',', ': '))
    except IOError:
        if not silent:
            messageBox(text='Cannot save .json file:\n{}'.format(filename))
        raise
    except StandardError:
        if not silent:
            messageBox(text='Unexpected error saving .json file:\n{}'.format(filename))
        raise

    return obj

#
