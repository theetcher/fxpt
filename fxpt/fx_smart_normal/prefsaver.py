import json

import maya.cmds as m


OPT_VAR_NAME = 'fx_smart_normals_prefs'


class PrefSaver(object):
    """
    :type params: fxpt.fx_smart_normal.ui.Parameters
    """
    def __init__(self, params):
        self.params = params

    def paramsToPrefs(self):
        d = {
            'curveThresh': self.params.curveThresh,
            'growAngle': self.params.growAngle,
            'dispCurve': self.params.dispCurve,
            'curveScale': self.params.curveScale,
        }
        self.saveToOptVar(d)

    def prefsToParams(self):
        d = self.loadFromOptVar()
        if d:
            self.params.curveThresh = d['curveThresh']
            self.params.growAngle = d['growAngle']
            self.params.dispCurve = d['dispCurve']
            self.params.curveScale = d['curveScale']

    @staticmethod
    def loadFromOptVar():
        if m.optionVar(exists=OPT_VAR_NAME):
            return json.loads(m.optionVar(q=OPT_VAR_NAME))
        else:
            return {}

    @staticmethod
    def saveToOptVar(d):
        m.optionVar(stringValue=(OPT_VAR_NAME, json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))))
