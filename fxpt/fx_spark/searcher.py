from . import harvester, annalist, cfg


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


from fxpt.fx_utils.watch import watch


class Searcher(object):
    def __init__(self):
        h = harvester.Harvester()
        self.db = h.harvest()
        self.annalist = annalist.Annalist()

    def search(self, s):
        s = s.strip().lower()
        if not s:
            return self.emptySearch()

        searchCategory = cfg.SEARCH_CATEGORY_TOOLS
        if s[0] in cfg.SPECIAL_SEARCHES:
            searchCategory = s[0]
            s = s[1:]

        return self.doSearch(searchCategory, s)

    def emptySearch(self):
        cmds = set(self.annalist.getFavoriteCommands()) | set(self.annalist.getRecentCommands())
        searchDb = self.db[cfg.SEARCH_CATEGORY_ALL]
        return [searchDb[c.lower()] for c in cmds if c.lower() in searchDb]

    def doSearch(self, searchCategory, s):
        searchDb = self.db[searchCategory]
        results = self.matched(s, searchDb)
        if not results:
            results = self.suggest(s, searchDb)
        return results

    # noinspection PyMethodMayBeStatic
    def variants(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits for c in ALPHABET if b]
        inserts = [a + c + b for a, b in splits for c in ALPHABET]
        res = set(deletes + transposes + replaces + inserts)
        return res

    # noinspection PyMethodMayBeStatic
    def matched(self, word, searchDb):
        return set(searchDb[key] for key in searchDb if word in key)

    def suggest(self, word, searchDb):
        return set([searchDb[key] for v in self.variants(word) for key in searchDb if v in key])

    def commandExecuted(self, desc):
        self.annalist.record(desc)
