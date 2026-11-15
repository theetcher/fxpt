import os
from fxpt3.side_utils import yaml

from fxpt3.fx_utils import message_box
from fxpt3.fx_utils.utils import makeWritable


def load(filename, showError=True, alertNotExist=True):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            obj = yaml.safe_load(f)
    except IOError:
        if alertNotExist and not os.path.exists(filename):
            message_box.exception('Cannot load YAML file. File does not exists:\n{}'.format(filename))
        if showError:
            message_box.exception('Cannot load YAML file:\n{}'.format(filename))
        raise
    except yaml.YAMLError:
        if showError:
            message_box.exception('Error parsing YAML file. Check syntax:\n{}'.format(filename))
        raise
    except Exception:
        if showError:
            message_box.exception('Unexpected error loading YAML file:\n{}'.format(filename))
        raise

    return obj


def dump(filename, obj, showError=True):
    try:
        makeWritable(filename)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(yaml.safe_dump(obj, default_flow_style=False, allow_unicode=True))
    except IOError:
        if showError:
            message_box.exception('Cannot save YAML file:\n{}'.format(filename))
        raise
    except Exception:
        if showError:
            message_box.exception('Unexpected error saving YAML file:\n{}'.format(filename))
        raise

