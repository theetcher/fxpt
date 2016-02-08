from . import json_io, cfg

KEY_RECENT = 'recent'
KEY_ACTIVITY = 'activity'

DEFAULT_DB = {
    KEY_RECENT: [],
    KEY_ACTIVITY: {}
}


class Annalist(object):
    def __init__(self):
        try:
            self.db = json_io.load(cfg.HISTORY_FILE, silent=True)
        except StandardError:
            self.db = DEFAULT_DB

    def record(self, desc):
        self.updateRecent(desc.name)
        self.updateActivity(desc.name)
        json_io.dump(cfg.HISTORY_FILE, self.db)

    def updateRecent(self, name):
        rList = self.db[KEY_RECENT]
        if name in rList:
            rList.remove(name)
        else:
            if len(rList) >= cfg.HISTORY_LENGTH:
                rList.pop()
        rList.insert(0, name)

    def updateActivity(self, name):
        aDict = self.db[KEY_ACTIVITY]
        if name in aDict:
            aDict[name] += 1
        else:
            aDict[name] = 1

    def getFavoriteCommands(self):
        return [item[0] for item in sorted(self.db[KEY_ACTIVITY].items(), key=lambda x: (-x[1], x[0]))][:cfg.HISTORY_LENGTH]

    def getRecentCommands(self):
        return self.db[KEY_RECENT]
