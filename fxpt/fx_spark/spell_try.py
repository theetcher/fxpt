def mayaCommandsDb(text):
    with open('maya_runtime_commands_list.txt', 'r') as f:
        return {c.strip().lower(): c.strip() for c in f.readlines()}


MAYA_COMMANDS_DB = mayaCommandsDb(file('maya_runtime_commands_list.txt').read())
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def variants(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in ALPHABET if b]
    inserts = [a + c + b for a, b in splits for c in ALPHABET]
    res = set(deletes + transposes + replaces + inserts)
    return res


def matched(word):
    return set(MAYA_COMMANDS_DB[c] for c in MAYA_COMMANDS_DB if word in c)


def suggest(word):
    return set([MAYA_COMMANDS_DB[c] for v in variants(word) for c in MAYA_COMMANDS_DB if v in c])


def getFromCommandsDb(word):
    word = word.lower()
    cmd = matched(word)
    print 'Matched directly: {}'.format(len(cmd))
    printList(cmd, '   ')
    if not cmd:
        cmd = suggest(word)
        print 'Matched guessing: {}'.format(len(cmd))
        printList(cmd, '   ')
    return sorted(cmd)


def printList(l, indent=''):
    for e in l:
        print indent, e


tryWords = [
    'freze',
    'freeze',
    'frz',
    'out',
    'outliner',
    'outlner'
]

if __name__ == '__main__':

    for tryW in tryWords:
        print
        print 'matching', tryW
        commands = getFromCommandsDb(tryW)
